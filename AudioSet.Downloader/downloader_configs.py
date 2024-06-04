from typing import List

CSV_FILE_NAMES: List[str] = [
    "filtered_database_reduced.csv",
]
YTB_URL_FORMAT: str = "https://www.youtube.com/watch?v={YTID}"
TIMER: int = -1  # using -1 , to download all
DOWN_HIGHEST_QUALITY: bool = True
REMOVE_EXIST_DOWNLOADS: bool = False
DEBUG: bool = False
# Experimental Features
ONLY_AUDIO: bool = False
DELETE_DOWNLOADED_VIDEO: bool = True
DELETE_WAVE_FILE: bool = True
CONCURRENT_TASKS: int = 5  # 每次并发处理的任务数，减少负载
POOL_SIZE = 2
USER_AGENT: str = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
LOG_FILE = "log.csv"