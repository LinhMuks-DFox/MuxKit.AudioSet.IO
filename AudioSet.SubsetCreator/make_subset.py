import json
import os
import shutil
from subset_maker_config import *

"""
Dataset structure:
    "0": {
        "path": "eval_segments_4000.csv.splits/--4gqARaEJE.wav",
        "onto": [
            "/m/068hy",
            "/m/07q6cd_",
            "/m/0bt9lr",
            "/m/0jbk"
        ],
        "label_digits": [
            "73",
            "361",
            "74",
            "72"
        ],
        "label_display": [
            "Domestic animals, pets",
            "Squeak",
            "Dog",
            "Animal"
        ]
    }
"""

with open(PATH_TO_TRAIN_JSON, "r") as t, open(PATH_TO_EVAL_PATH, "r") as e:
    train_data_json = json.load(t)
    eval_data_json = json.load(e)

sub_train_json = {}
sub_train_statistic = {
    key: 0 for key in SELECTED_LABELS.keys()
}
sub_eval_json = {}
sub_eval_statistic = {
    key: 0 for key in SELECTED_LABELS.keys()
}


def make_json(data_json, sub_json, sub_statistic):
    iota = 0
    for key, value in data_json.items():
        if len(union := (set(value["label_digits"]) & set(SELECTED_LABELS.keys()))) >= 1:
            union = list(union)[0]
            sub_statistic[union] += 1
            sub_json[iota] = {
                "path": value["path"],
                "onto": SELECTED_LABELS[union]["onto"],
                "label_display": SELECTED_LABELS[union]["name"],
                "label_digits": SELECTED_LABELS[union]["label_digits"]
            }
            print(f"Added {key}({value['path']}, {value['label_display']}) to subset.")
            print(f"Union: {union}")
            iota += 1


with open("sub_train.json", "w") as st, open("sub_eval.json", "w") as se, open("description.txt", "w") as d:
    make_json(train_data_json, sub_train_json, sub_train_statistic)
    make_json(eval_data_json, sub_eval_json, sub_eval_statistic)
    json.dump(sub_train_json, st, indent=4)
    json.dump(sub_eval_json, se, indent=4)

    for k, v in SELECTED_LABELS.items():
        d.write("label {}: \n\t"
                "onto: {}\n\t"
                "display name: {}\n\t"
                "sample count(train:{}, eval:{})\n\t"
                "label_digits: {}\n".format(k, v["onto"], v["name"],
                                            sub_train_statistic[k],
                                            sub_eval_statistic[k], v["label_digits"]))

    d.write("Train dataset length: {}\n".format(len(sub_train_json)))
    d.write("Eval dataset length: {}\n".format(len(sub_eval_json)))

# move files
if os.path.exists("subset_json"):
    shutil.rmtree("subset_json")
os.mkdir("subset_json")
shutil.move("sub_train.json", "subset_json")
shutil.move("sub_eval.json", "subset_json")
shutil.move("description.txt", "subset_json")
