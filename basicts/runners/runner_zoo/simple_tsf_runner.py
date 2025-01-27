# import os

import numpy as np
import torch

from ..base_tsf_runner import BaseTimeSeriesForecastingRunner

from basicts.data.transform import re_standard_transform


class SimpleTimeSeriesForecastingRunner(BaseTimeSeriesForecastingRunner):
    """Simple Runner: select forward features and target features."""

    def __init__(self, cfg: dict):
        super().__init__(cfg)
        self.forward_features = cfg["MODEL"].get("FORWARD_FEATURES", None)
        self.target_features = cfg["MODEL"].get("TARGET_FEATURES", None)

    def select_input_features(self, data: torch.Tensor) -> torch.Tensor:
        """Select input features.

        Args:
            data (torch.Tensor): input history data, shape [B, L, N, C]

        Returns:
            torch.Tensor: reshaped data
        """

        # select feature using self.forward_features
        if self.forward_features is not None:
            data = data[:, :, :, self.forward_features]
        return data

    def select_target_features(self, data: torch.Tensor) -> torch.Tensor:
        """Select target feature.

        Args:
            data (torch.Tensor): prediction of the model with arbitrary shape.

        Returns:
            torch.Tensor: reshaped data with shape [B, L, N, C]
        """

        # select feature using self.target_features
        data = data[:, :, :, self.target_features]
        return data

    def forward(self, data: tuple, epoch: int = None, iter_num: int = None, train: bool = True, **kwargs) -> tuple:
        """Feed forward process for train, val, and test. Note that the outputs are NOT re-scaled.

        Args:
            data (tuple): data (future data, history ata).
            epoch (int, optional): epoch number. Defaults to None.
            iter_num (int, optional): iteration number. Defaults to None.
            train (bool, optional): if in the training process. Defaults to True.

        Returns:
            tuple: (prediction, real_value)
        """

        # preprocess
        future_data, history_data = data
        history_data = self.to_running_device(history_data)      # B, L, N, C
        future_data = self.to_running_device(future_data)       # B, L, N, C
        batch_size, length, num_nodes, _ = future_data.shape

        history_data = self.select_input_features(history_data)
        future_data_4_dec = self.select_input_features(future_data)

        # curriculum learning
        if self.cl_param is None:
            prediction_data = self.model(history_data=history_data, future_data=future_data_4_dec, batch_seen=iter_num, epoch=epoch, train=train)
        else:
            task_level = self.curriculum_learning(epoch)
            prediction_data = self.model(history_data=history_data, future_data=future_data_4_dec, batch_seen=iter_num, epoch=epoch, train=train,\
                                                                                                                     task_level=task_level)
        # feed forward
        assert list(prediction_data.shape)[:3] == [batch_size, length, num_nodes], \
            "error shape of the output, edit the forward function to reshape it to [B, L, N, C]"
        # post process
        prediction = self.select_target_features(prediction_data)
        real_value = self.select_target_features(future_data)

        if not train:
            # print('prediction.type: ' + str(type(prediction)))
            print('prediction.shape: ' + str(prediction.shape))
            # print('real_value.type: ' + str(type(real_value)))
            print('real_value.shape: ' + str(real_value.shape))
            #
            # print(os.getcwd())

            # the mean and std need to be manually updated from generate_training_data
            scaler = {"mean": 3.25250095456281, "std": 5.547118144526464}

            error_scaler = {"mean": 0, "std": 5.547118144526464}

            prediction_path = 'checkpoints/tensorCsv/scooter_prediction.npy'
            np.save(prediction_path, re_standard_transform(prediction, **scaler).cpu().data.numpy())

            real_value_path = 'checkpoints/tensorCsv/scooter_real_value.npy'
            np.save(real_value_path, re_standard_transform(real_value, **scaler).cpu().data.numpy())

            prediction_error = torch.sub(prediction, real_value)
            prediction_error_path = 'checkpoints/tensorCsv/prediction_error.npy'
            np.save(prediction_error_path, re_standard_transform(prediction_error, **error_scaler).cpu().data.numpy())

            print('Test error updated')

        return prediction, real_value
