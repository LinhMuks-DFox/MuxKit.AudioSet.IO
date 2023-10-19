from typing import Dict
import pathlib

PATH_TO_TRAIN_JSON: pathlib.Path = pathlib.Path(r"F:\DataSets\Audioset\balanced\segments\AudioSet.json")
PATH_TO_EVAL_PATH: pathlib.Path = pathlib.Path(r"F:\DataSets\Audioset\eval\segments\AudioSet.json")
DRY_RUN: bool = False
SUB_SET_SAMPLE_COUNT: int = 20000 // 10
PACK: bool = True
RANDOM_SEED: int = 42

SELECTED_LABELS: Dict[str, Dict] = {
    "2": {"name": "Female Speech", "onto": "/m/02zsn"},  # 50
    "141": {"name": "Electric guitar", "onto": "/m/02sgy"},  # 60
    "351": {"name": "Engine staring", "onto": "/t/dd00130"},  # 55
    "352": {"name": "idling", "onto": "/m/07pb8fc"},  # 58
    "395": {"name": "Alarm clock", "onto": "/m/046dlr"},  # 50
    "426": {"name": "Explosion", "onto": "/m/014zdl"},  # 53
    "119": {"name": "Owl", "onto": "/m/09d5_"},  # 57
    "122": {"name": "Canidae, dogs, wolve", "onto": "/m/01z5f"},  # 53
    "287": {"name": "Thunder", "onto": "/m/0ngt1"},  # 57
    "294": {"name": "Ocean", "onto": "/m/05kq4"},  # 64
}

SINGLE_LABEL: bool = True
