import os

csv_in = "long_wav_files.csv"

lines = None
with open(csv_in, "r") as f:
    lines = f.readlines()
    
for line in lines:
    line = line.split(",")[0]
    os.remove((n:=os.path.join("filtered_database_reduced.csv.splits", line)))
    print(n, "removed")
    # print(os.path.exists(os.path.join("filtered_database_reduced.csv.splits", line)))
    