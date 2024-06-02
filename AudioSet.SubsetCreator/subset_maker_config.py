import json
from typing import Dict
import pathlib

PATH_TO_TRAIN_JSON: pathlib.Path = pathlib.Path(r"F:\DataSets\Audioset\balanced\segments\AudioSet.json")
PATH_TO_EVAL_PATH: pathlib.Path = pathlib.Path(r"F:\DataSets\Audioset\eval\segments\AudioSet.json")


# SELECTED_LABELS: Dict[str, Dict] = {
#     "2": {"name": "Female Speech", "onto": "/m/02zsn", "label_digits": [0, ]},  # 50
#     "141": {"name": "Electric guitar", "onto": "/m/02sgy", "label_digits": [1, ]},  # 60
#     "351": {"name": "Engine staring", "onto": "/t/dd00130", "label_digits": [2, ]},  # 55
#     "352": {"name": "idling", "onto": "/m/07pb8fc", "label_digits": [3, ]},  # 58
#     "395": {"name": "Alarm clock", "onto": "/m/046dlr", "label_digits": [4, ]},  # 50
#     "426": {"name": "Explosion", "onto": "/m/014zdl", "label_digits": [5, ]},  # 53
#     "119": {"name": "Owl", "onto": "/m/09d5_", "label_digits": [6, ]},  # 57
#     "122": {"name": "Canidae, dogs, wolve", "onto": "/m/01z5f", "label_digits": [7, ]},  # 53
#     "287": {"name": "Thunder", "onto": "/m/0ngt1", "label_digits": [8, ]},  # 57
#     "294": {"name": "Ocean", "onto": "/m/05kq4", "label_digits": [9, ]},  # 64
# }
# SELECTED_LABELS: Dict[str, Dict] = {
#     "0": {"name": "Speech", "onto": "/m/09x0r", "label_digits": [0, ]},
#     "137": {"name": "Music", "onto": "/m/04rlf", "label_digits": [1, ]},
# }
SELECTED_LABELS: Dict[str, Dict] = {
    "200": {"name": "Bell", "onto": "/m/0395lw", "label_digits": [0, ]},
    "388": {"name": "Alarm", "onto": "/m/07pp_mv", "label_digits": [1, ]},
}


SINGLE_LABEL: bool = True
