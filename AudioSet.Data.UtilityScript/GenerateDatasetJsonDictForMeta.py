"""
Author: LinhMuks
Date: 2023-7-23(last updated)
Same function as GenerateDatasetJsonDictForSplitMetaCSV.py, but this one is for meta data(files in AudioSet.Meta).

This format json file will be genrated:
{
    "{iota}" : {
        "youtube_id": "{youtube_id}",
        "start_seconds": "{start_seconds}",
        "end_seconds": "{end_seconds}",
        "positive_labels": [
            "onto" : "{onto}",
            "label_digits": []
            "label_display": []
        ]
    }
}

"""
import json
import csv
import typing

FILE_IN = r"../AudioSet.Meta/unbalanced_train_segments.csv"
FILE_OUT = r"../AudioSet.Meta/unbalanced_train_segments.json"
CLS_LABEL_INDICES = "./class_labels_indices.json"


def clean_onto(onto: typing.List[str]) -> list:
    splits: typing.List[str] = sum([(i.split(",")) for i in onto], [])
    splits: typing.List[str] = [i.replace(" ", "").replace('"', '') for i in splits]
    return splits


def main():
    with open(FILE_IN, "r") as f_in, \
            open(FILE_OUT, "w") as f_out, \
            open(CLS_LABEL_INDICES, "r") as f_cls_label:
        csv_reader = csv.reader(f_in)
        label_dict = json.load(f_cls_label)
        json_content = dict()
        iota = 0
        for row in csv_reader:
            ytid = row[0]
            start_sec = row[1]
            end_sec = row[2]
            onto = clean_onto(row[3:])
            label_digits = [label_dict[i]["index"] for i in onto]
            label_dis = [label_dict[i]["display_name"] for i in onto]
            iota_content = {
                "youtube_id": ytid,
                "start_seconds": start_sec,
                "end_seconds": end_sec,
                "positive_labels": {
                    "onto": onto,
                    "label_digits": label_digits,
                    "label_display": label_dis
                }
            }
            json_content[iota] = iota_content
            iota += 1

            if iota % 10 == 0:
                print("Producing iota: ", iota)
        print("Dumping....")
        json.dump(json_content, f_out, indent=4)
        print("Done")


if __name__ == "__main__":
    main()
