# Work Flow



#### 1. Download Metadata 

Download the metadata for audio set, a file in csv format. This includes four pieces of information:

| YOUTUBE VIDEO ID | START SECOUND | END SECOUND | LABELS(See ontology) |
| :--------------: | :-----------: | :---------: | :------------------: |
|   --PJHxphWEs    |    30.000     |   40.000    | /m/09x0r,/t/dd00088  |

YouTube Video Id is the unique id of the YouTube video, format it into the YouTube URL format to access the video resource.

In the` AudioSet.Meta` folder, there are preprocessed csv files. The contents are the same as the original csv file, except that the three lines of descriptive information at the very beginning have been removed.

The csv file for the dataset is large, with more than 20,000 data, and the data for the unbalanced training set is around two million. It is therefore recommended to use the `SplitCSV.py` script in `AudioSet.Data.UtilityScript` to split individual csv files.

The `AudioSet.Downloader` provided in this project creates download processes for files. A csv file corresponds to a download process.

#### 2. Dataset Dictionary Creation

The `AudioSet.Downloader` will download the video based on the csv file and cut out the segment, then create another csv file containing only the filename as well as the tag information. Csv file reading is not programmatically easy to manipulate, so it is recommended to use the  `GenerateDatasetJsonDictForSplitMetaCSV.py` script in the `AudioSet.Data.UtilityScript` to create the corresponding dataset dictionary in json format.

CSV file:

```csv
--PJHxphWEs.wav, "/m/09x0r,/t/dd00088"
```

 Corresponding json: 

```json
"0": {
    "path": "balanced_train_segments4000.csv.splits/--PJHxphWEs.wav",
    "onto": [
        "/m/09x0r",
        "/t/dd00088"
    ],
    "label_digits": [
        "0",
        "451"
    ],
    "label_display": [
        "Speech",
        "Gush"
    ]
},
```

Where iota(=`"0"`) is the index of the data. 

The Downloader creates a one-to-one download directory for csv files, in this case `balanced_train_segments4000.csv.splits`, path is the relative path from the json file to the sample.

`onto` is shorthand for ontology, which is the sample labeling information provided by the audio set dataset. It is described using a string of text that has been encoded.

According to the label descriptions provided by the audio set, `label_digits` holds the number of the label, and `label_display` holds the label in a human-readable text format.

正因如此，本项目中的`AudioSet.IO.JsonBasedAudioSet`在被下标访问数据时，会返回5个信息：

* Data Sampling Itself

* Data Sampling Rate
* Data Ontology
* Numeric Labeling of Data
* Text Labeling of Data

#### 3. Use AudioSet

```python
from AudioSet.IO import JsonBasedAudioSet as jba

data_dict_json_path = r"path/to/json/file/created/in/process/2/AudioSet.json"
dataset = jba.JsonBasedAudioSet(data_dict_json_path)
sample, sr, onto, label_digit, lable_str = dataset[0]
```

