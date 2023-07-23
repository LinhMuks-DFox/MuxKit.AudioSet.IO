"""
Author: LinhMuks
Date: 2023-7-23 (last update)
Function:
    Find out the useless audio files and remove them.
Default Rule:
    1. The audio file is empty.
"""

import torch
from AudioSetIO.JsonBasedAudioSet import JsonBasedAudioSet
import train_config as config


def remove_able(audio_data: torch.Tensor) -> bool:
    return audio_data.shape[1] == 0


data_set = JsonBasedAudioSet(config.DATA_PATH)

removes = []
for idx in range(len(data_set)):  # enumerate(data_set) not work crrectly
    sample, _ = data_set[idx]
    if remove_able(sample):
        removes.append(data_set.splice_audio_path(idx))
        print(f"sample {removes[-1]} shall be removed, data shape: {sample.shape}")

    if idx % 100 == 0:
        print(f"Processed {idx} samples")

if len(removes) != 0:
    with open("RemovableSamples.txt", "w") as remove_sample:
        remove_sample.write("\n".join(removes))
