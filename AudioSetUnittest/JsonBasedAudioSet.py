import os.path
import unittest

from AudioSet.IO import JsonBasedAudioSet


class MyTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.json_path = "../data/audio_set/AudioSet.json"
        self.audio_sample_folder = "../data/audio_set"
        self.jbAudioSet = JsonBasedAudioSet(self.json_path)
        self.excepted_length = 80 + 1

    def test_length(self):
        self.assertEqual(len(self.jbAudioSet), self.excepted_length)

    def test_get_item(self):
        idx = 232
        sample, sample_rate, onto, label_digits, label_display = self.jbAudioSet[idx]
        print("sample:", sample)
        print("sample rate:", sample_rate)
        print("ontology:", onto)

    def test_splice_item(self):
        idx = 232
        excepted_file_name = os.path.join(self.audio_sample_folder,
                                          "balanced_train_segments4000.csv.splits/-ZjxFZOaY50.wav")
        self.assertEqual(self.jbAudioSet.splice_audio_path(idx), excepted_file_name)


if __name__ == '__main__':
    unittest.main()
