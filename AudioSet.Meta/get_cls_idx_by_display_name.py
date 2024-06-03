import pandas as pd

# Load the CSV file
file_path = './class_labels_indices.csv'  # replace with the actual file path
df = pd.read_csv(file_path)

# List of categories to find
categories = [
    "Insect", "Drum roll", "Bicycle", "Skateboard", "Fireworks", "Spray", 
    "Ocean", "Power tool", "Horse", "Rain", "Vocal music", "Cat", "Radio", 
    "Run", "Wind", "Dog", "Bird", "Train", "Crowd", "Engine"
]

# Search for the categories in the display_name column
results = df[df['display_name'].isin(categories)]

# Output the corresponding index and mid values
for index, row in results.iterrows():
    print(f"Category: {row['display_name']}, Index: {row['index']}, MID: {row['mid']}")

# Save results to a new CSV file
results.to_csv('found_categories.csv', index=False)
