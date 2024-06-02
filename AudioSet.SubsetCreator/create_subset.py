import json
import csv
from tqdm import tqdm

# File paths
ontology_file_path = 'found_categories.csv'
database_json_path = 'unbalanced_train_segments.json'
output_csv_path = 'filtered_database.csv'
count_summary_path = 'count_summary.csv'

# Load ontologies of interest
interest_ontologies = {}
with open(ontology_file_path, mode='r', newline='', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:
        interest_ontologies[row['mid']] = {'display_name': row['display_name'], 'count': 0}

# Process the large JSON database
results = []
max_samples = 3000

with open(database_json_path, 'r', encoding='utf-8') as file:
    database = json.load(file)
    for key, entry in tqdm(database.items(), desc="Processing Database"):
        # Check for matching ontologies
        if any(onto in interest_ontologies for onto in entry['positive_labels']['onto']):
            matched_ontos = [onto for onto in entry['positive_labels']['onto'] if onto in interest_ontologies]
            for onto in matched_ontos:
                if interest_ontologies[onto]['count'] < max_samples:
                    results.append({
                        'youtube_id': entry['youtube_id'],
                        'start_seconds': entry['start_seconds'].strip(),
                        'end_seconds': entry['end_seconds'].strip(),
                        'onto': onto
                    })
                    interest_ontologies[onto]['count'] += 1

# Write results to a new CSV file
with open(output_csv_path, mode='w', newline='', encoding='utf-8') as file:
    fieldnames = ['youtube_id', 'start_seconds', 'end_seconds', 'onto']
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    for result in results:
        writer.writerow(result)

# Write category count summary
with open(count_summary_path, mode='w', newline='', encoding='utf-8') as file:
    fieldnames = ['index', 'mid', 'display_name', 'count']
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    for idx, (mid, info) in enumerate(interest_ontologies.items()):
        writer.writerow({'index': idx, 'mid': mid, 'display_name': info['display_name'], 'count': info['count']})

print("Processing complete. Output files generated.")
