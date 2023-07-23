"""
Author: LinhMuks
Date: 2023-7-23 (last update)
Function: Split the csv file into smaller files.

"""
LINES_PER_FILE = 4000
TARGET_CSV_FILE = "balanced_train_segments.csv"


def main():
    smallfile = None
    with open(TARGET_CSV_FILE) as bigfile:
        for lineno, line in enumerate(bigfile):
            if lineno % LINES_PER_FILE == 0:
                if smallfile:
                    smallfile.close()
                small_filename = 'balanced_train_segments{}.csv'.format(lineno + LINES_PER_FILE)
                smallfile = open(small_filename, "w")
            smallfile.write(line)
        if smallfile:
            smallfile.close()


if __name__ == "__main__":
    main()
