import csv


def split_csv(input_file, output_file_prefix, chunk_size):
    with open(input_file, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        headers = next(reader)  # 读取表头
        chunk_number = 1
        current_chunk = []

        for i, row in enumerate(reader, 1):
            current_chunk.append(row)
            if i % chunk_size == 0:
                output_file = f"{output_file_prefix}{chunk_number}.csv"
                with open(output_file, 'w', newline='') as output_csvfile:
                    writer = csv.writer(output_csvfile)
                    writer.writerow(headers)  # 写入表头
                    writer.writerows(current_chunk)
                print(f"{output_file} has been created.")
                chunk_number += 1
                current_chunk = []

        # 处理最后一块未满chunk_size的行
        if current_chunk:
            output_file = f"{output_file_prefix}{chunk_number}.csv"
            with open(output_file, 'w', newline='') as output_csvfile:
                writer = csv.writer(output_csvfile)
                writer.writerow(headers)  # 写入表头
                writer.writerows(current_chunk)
            print(f"{output_file} has been created.")


input_file = 'unbalanced_train_segments.csv'
output_file_prefix = 'unbalanced_train_segments_'
chunk_size = 88773

split_csv(input_file, output_file_prefix, chunk_size)
