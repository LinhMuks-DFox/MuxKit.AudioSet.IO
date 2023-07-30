import unittest

import torchaudio

from AudioSet.IO.JsonBasedAudioSet import JsonBasedAudioSet as AudioSet
from src import transforms


class TimeSequenceLengthFixingTransformerTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.dataset1 = AudioSet("../data/AudioSet.json")
        self.dataset2 = AudioSet("../data/AudioSet_16k_mono")
        self.length = 5
        self.audio_sample_rate = 44100
        self.audio_sample_rate2 = 16000

        self.transformer = transforms.TimeSequenceLengthFixingTransformer(self.length, self.audio_sample_rate)
        self.transformer2 = transforms.TimeSequenceLengthFixingTransformer(self.length, self.audio_sample_rate2)
        self.excepted_length = self.length * self.audio_sample_rate
        self.excepted_length2 = self.length * self.audio_sample_rate2

    def test_transform(self):
        audio, sample_rate = self.dataset1[0]
        audio = self.transformer(audio)
        print(audio.shape)
        self.assertEqual(audio.shape[1], self.excepted_length)
        self.assertEqual(sample_rate, self.audio_sample_rate)

        audio, sample_rate = self.dataset2[0]
        audio = self.transformer2(audio)
        print(audio.shape)
        self.assertEqual(audio.shape[1], self.excepted_length2)
        self.assertEqual(sample_rate, self.audio_sample_rate2)


class SoundTrackSelectingTransformerTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.dataset1 = AudioSet("../data/AudioSet_Raw")
        self.select_mode = "left"
        self.transformer = transforms.SoundTrackSelectingTransformer(self.select_mode)

    def test_transform(self):
        audio, sample_rate = self.dataset1[0]
        audio = self.transformer(audio)
        print(audio.shape)
        if self.select_mode in ["all", "mix"]:
            self.assertEqual(audio.shape[0], 2)
        elif self.select_mode in ["left", "right"]:
            self.assertEqual(audio.shape[0], 1)


class TimeSequenceMaskingTransformerTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.dataset1 = AudioSet("../data/AudioSet_Raw")
        self.mask_rate = 0.8
        self.transformer = transforms.TimeSequenceMaskingTransformer(self.mask_rate)

    def test_transform(self):
        audio, sample_rate = self.dataset1[0]
        masked_audio, unmasked_audio = self.transformer(audio)
        print(masked_audio.shape)
        print(unmasked_audio.shape)
        self.assertEqual(masked_audio.shape, unmasked_audio.shape)


class SpectrogramMaskingTransformerTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.dataset1 = AudioSet("../data/AudioSet_Raw")
        self.mask_rate = 0.8
        self.spectrogram_transformer = torchaudio.transforms.Spectrogram(n_fft=2048, hop_length=512)
        self.transformer = transforms.SpectrogramMaskingTransformer(self.mask_rate)

    def test_transform(self):
        audio, sample_rate = self.dataset1[0]
        spectrogram = self.spectrogram_transformer(audio)
        masked_spectrogram, unmasked_spectrogram = self.transformer(spectrogram)
        print(masked_spectrogram.shape)
        print(unmasked_spectrogram.shape)
        self.assertEqual(masked_spectrogram.shape, unmasked_spectrogram.shape)


if __name__ == '__main__':
    unittest.main()
