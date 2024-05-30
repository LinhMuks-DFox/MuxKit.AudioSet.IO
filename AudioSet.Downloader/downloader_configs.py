from typing import List

CSV_FILE_NAMES: List[str] = [
    "unbalanced_train_segments_1.csv",
    "unbalanced_train_segments_2.csv",
    "unbalanced_train_segments_3.csv",
    "unbalanced_train_segments_4.csv",
    "unbalanced_train_segments_5.csv",
    "unbalanced_train_segments_6.csv",
    "unbalanced_train_segments_7.csv",
    "unbalanced_train_segments_8.csv",
    "unbalanced_train_segments_9.csv",
    "unbalanced_train_segments_10.csv",
    "unbalanced_train_segments_11.csv",
    "unbalanced_train_segments_12.csv",
    "unbalanced_train_segments_13.csv",
    "unbalanced_train_segments_14.csv",
    "unbalanced_train_segments_15.csv",
    "unbalanced_train_segments_16.csv",
    "unbalanced_train_segments_17.csv",
    "unbalanced_train_segments_18.csv",
    "unbalanced_train_segments_19.csv",
    "unbalanced_train_segments_20.csv",
    "unbalanced_train_segments_21.csv",
    "unbalanced_train_segments_22.csv",
    "unbalanced_train_segments_23.csv",
    "unbalanced_train_segments_24.csv"
]
YTB_URL_FORMAT: str = "https://www.youtube.com/watch?v={YTID}"
TIMER: int = 5  # using -1 , to download all
DOWN_HIGHEST_QUALITY: bool = True
REMOVE_EXIST_DOWNLOADS: bool = True
DEBUG: bool = True
# Experimental Features
ONLY_AUDIO: bool = False
DELETE_DOWNLOADED_VIDEO: bool = True
DELETE_WAVE_FILE: bool = True
