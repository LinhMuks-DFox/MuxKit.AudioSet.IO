"""
Author: LinhMuks
Date: 2023-7-23 (last update)
Function:
    Convert class_label_indices.csv to json file, using mid as key
    CSV file format(see csv file in AudioSet.Meta):
        index, mid, display_name
        0, /m/09x0r, Speech

    Json file format:
    {
       "mid": {
          "display_name": "display_name",
          "index": "index"
       }
    }
"""
import csv
import json

CLASS_LABEL_INDICES = "class_labels_indices.csv"
JSON_FILE_NAME = "class_labels_indices.json"

json_content = dict()
csv_reader = csv.reader(f_in := open(CLASS_LABEL_INDICES, "r"))

for row in csv_reader:
    json_content[row[0]] = {
        "display_name": row[2],
        "mid": row[1],
    }

f_out = open(JSON_FILE_NAME, "w")
json.dump(json_content, f_out, indent=4)
f_out.close()
f_in.close()
