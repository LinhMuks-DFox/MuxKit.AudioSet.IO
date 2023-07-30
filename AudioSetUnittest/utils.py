import os
import unittest

import numpy as np
import torch
import torchaudio

from AudioSet.utils import tensor_masking, create_mask, \
    plot_waveform, plot_spectrogram, create_mask_chunk_2d, \
    shape_after_conv, shape_after_conv_transpose, \
    shape_after_n_time_convolution, shape_after_n_time_convolution_transpose


class UtilsTest(unittest.TestCase):
    def setUp(self) -> None:
        self.audio_sample = "../data/AudioSet_16k_mono/1.wav"

    # Done
    def test_tensor_masking(self):
        data = torch.Tensor([
            [1, 1, 4],
            [5, 1, 4],
            [1, 9, 1],
            [9, 8, 1]
        ])

        masked_audio, unmasked, mask = tensor_masking(data)
        print(f"{data.shape}, {masked_audio.shape}, {unmasked.shape}, {mask.shape}")
        self.assertEqual(data.shape, masked_audio.shape)
        self.assertEqual(masked_audio.shape, unmasked.shape)
        self.assertEqual(masked_audio.shape, mask.shape)
        print(data)
        print(masked_audio)
        print(unmasked)
        print(mask)

        mask = create_mask(data.shape, .9)
        masked_audio, unmasked, mask = tensor_masking(data, mask=mask)
        print(f"{data.shape}, {masked_audio.shape}, {unmasked.shape}, {mask.shape}")
        self.assertEqual(data.shape, masked_audio.shape)
        self.assertEqual(masked_audio.shape, unmasked.shape)
        self.assertEqual(masked_audio.shape, mask.shape)
        print(data)
        print(masked_audio)
        print(unmasked)
        print(mask)

    # Done
    def test_plot_spectrogram(self):
        audio_data, sr = torchaudio.load(self.audio_sample)
        self.assertEqual(sr, 16000)
        plot_spectrogram(audio_data, sr)

    # Done
    def test_plot_waveform(self):
        audio_data, sr = torchaudio.load(self.audio_sample)
        self.assertEqual(sr, 16000)
        plot_waveform(audio_data, sr)

    # Done
    @staticmethod
    def test_create_mask_chunk_2d():
        t = torch.randint(low=0, high=9, size=(4, 4))
        mask = create_mask_chunk_2d(t.shape, 0.2, 2)
        print("Org:", t)
        audio_masked, audio_unmasked, mask = tensor_masking(t, mask=mask)
        print("Mask:", mask)
        print("Masked", audio_masked)
        print("Unmasked", audio_unmasked)

    # Done
    def test_shape_after_conv_nd(self):
        conv_kernel_size = np.array([7, 7])
        conv_padding = np.array([0, 0])
        conv_stride = np.array([1, 1])
        conv_dilation = np.array([1, 1])
        shape = np.array([28, 28])
        shape = shape_after_conv(shape,
                                 kernel_size=conv_kernel_size,
                                 padding=conv_padding,
                                 stride=conv_stride,
                                 dilation=conv_dilation)
        self.assertEqual(np.all(shape == np.array([22, 22])), True)
        conv_kernel_size = np.array([3, 3])
        shape = shape_after_conv(shape,
                                 kernel_size=conv_kernel_size,
                                 padding=conv_padding,
                                 stride=conv_stride,
                                 dilation=conv_dilation)
        self.assertEqual(np.all(shape == np.array([20, 20])), True)

        conv_kernel_size = np.array([7, 7])
        conv_padding = np.array([0, 0])
        conv_stride = np.array([1, 1])
        conv_dilation = np.array([1, 1])
        shape = np.array([1, 28])
        shape = shape_after_conv(shape,
                                 kernel_size=conv_kernel_size,
                                 padding=conv_padding,
                                 stride=conv_stride,
                                 dilation=conv_dilation)
        print(shape)

    # Done
    def test_shape_after_conv_nd_trans(self):
        conv_kernel_size = np.array([3, 3])
        conv_padding = np.array([0, 0])
        conv_stride = np.array([1, 1])
        conv_dilation = np.array([1, 1])
        shape = np.array([20, 20])
        shape = shape_after_conv_transpose(shape,
                                           kernel_size=conv_kernel_size,
                                           padding=conv_padding,
                                           stride=conv_stride,
                                           dilation=conv_dilation)
        self.assertEqual(np.all(shape == np.array([22, 22])), True)
        conv_kernel_size = np.array([7, 7])
        shape = shape_after_conv_transpose(shape,
                                           kernel_size=conv_kernel_size,
                                           padding=conv_padding,
                                           stride=conv_stride,
                                           dilation=conv_dilation)
        self.assertEqual(np.all(shape == np.array([28, 28])), True)

        if __name__ == "__main__":
            unittest.main()

    def test_shape_after_n_time_convolution(self):
        conv_kernel_size = np.array([[3, 3],
                                     [7, 7]])
        conv_padding = np.array([[0, 0],
                                 [0, 0]])
        conv_stride = np.array([[1, 1],
                                [1, 1]])
        conv_dilation = np.array([[1, 1],
                                  [1, 1]])
        shape = np.array([28, 28])
        conv_n_time = 2

        shape = shape_after_n_time_convolution(
            shape,
            conv_kernel_size,
            conv_n_time,
            conv_padding,
            conv_stride,
            conv_dilation
        )
        self.assertEqual(np.all(shape == np.array([20, 20])), True)

    def test_shape_after_n_time_convolution_transpose(self):
        conv_kernel_size = np.array([[3, 3],
                                     [7, 7]])
        conv_padding = np.array([[0, 0],
                                 [0, 0]])
        conv_stride = np.array([[1, 1],
                                [1, 1]])
        conv_dilation = np.array([[1, 1],
                                  [1, 1]])
        shape = np.array([20, 20])
        conv_n_time = 2

        shape = shape_after_n_time_convolution_transpose(
            shape,
            conv_kernel_size,
            conv_n_time,
            conv_padding,
            conv_stride,
            conv_dilation
        )
        self.assertEqual(np.all(shape == np.array([28, 28])), True)
