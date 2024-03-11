# AudioSet.SubsetCreator

Designed to create subsets of the [AudioSet](https://research.google.com/audioset/) dataset.

### Usage

1. Fix the AudioSet.json file path in the `subset_maker_config.py` file.
2. Define the subset you need.

   For example: 

   Suppose you need a subset containing "Bell" and "Alarm":
   
   - Go to the AudioSet.Meta folder and find the file `class_labels_indices.csv`.
   - Search for "Bell". You'll find it as follows: `200,/m/0395lw,"Bell"`.
   - Search for "Alarm". You'll find it as follows: `388,/m/07pp_mv,"Alarm"`.
   - Redefine the variable `SELECTED_LABELS: Dict[str, Dict]` contained in `subset_maker_config.py` as follows:
   
    ```Python
    SELECTED_LABELS: Dict[str, Dict] = {
       "200": {"name": "Bell", "onto": "/m/0395lw", "label_digits": [0, ]},
       "388": {"name": "Alarm", "onto": "/m/07pp_mv", "label_digits": [1, ]},
    }
    ```

3. Run `make_subset.py`.

### Caution

The variable `SELECTED_LABELS`, is a dictionary that maps string keys to dictionary values. Each key represents a label ID associated with audio classes in the AudioSet dataset. The corresponding dictionary value contains metadata about the audio class represented by that label ID. The metadata includes the following information:

- `"name"`: The human-readable name of the audio class (e.g., "Bell", "Alarm").
- `"onto"`: The ontology ID associated with the audio class.
- `"label_digits"`: A list of integers representing the label digits associated with the audio class.

For example:

```python
SELECTED_LABELS = {
   "200": {"name": "Bell", "onto": "/m/0395lw", "label_digits": [0]},
   "388": {"name": "Alarm", "onto": "/m/07pp_mv", "label_digits": [1]},
}

```

In this example, the audio classes "Bell" and "Alarm" are defined with their respective metadata within the `SELECTED_LABELS` dictionary. Each audio class is identified by a unique label ID (e.g., "200" for "Bell" and "388" for "Alarm"), and the associated metadata provides additional information about each class.

This structure facilitates the organization and selection of specific audio classes when creating subsets of the AudioSet dataset.
