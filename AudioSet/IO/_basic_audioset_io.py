import os
from typing import Tuple, List

import torch
import torchaudio
from torch.utils.data import Dataset


class AudioSet(Dataset):

    def __init__(self, audio_set_dir: str) -> None:
        if not os.path.exists(audio_set_dir):
            raise IOError(f"AudioSet directory not found: <{audio_set_dir}>")

        self.audio_dir_: str = audio_set_dir
        self.audio_list_: List[str] = os.listdir(self.audio_dir_)

    def __len__(self):
        return len(self.audio_list_)

    def __getitem__(self, idx: int) -> Tuple[torch.Tensor, int]:
        audio_path = self._splice_audio_path(idx)
        audio_data, sample_rate = torchaudio.load(audio_path)
        return audio_data, sample_rate

    def _splice_audio_path(self, idx: int):
        if idx > len(self):
            raise IndexError(f"Index({idx}) out of range{f'0 ~ {len(self)}'}")
        return os.path.join(self.audio_dir_, self.audio_list_[idx])

    def __repr__(self):
        return f"AudioSet: {len(self)} items"


if __name__ == "__main__":
    set = AudioSet("../data/AudioSet_Raw/")
    print(set[0][0].shape, set[0][1])
