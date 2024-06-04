import pandas as pd
from tqdm import tqdm

# 手动指定列名
column_names = ['youtube_id', 'start_second', 'end_second', 'onto']

# 文件路径
file_path = 'filtered_database.csv'
output_path = 'filtered_database_reduced.csv'
report_path = 'duplicates_report_reduced.txt'

def process_chunk(chunk):
    chunk['onto'] = chunk.groupby(['youtube_id', 'start_second', 'end_second'])['onto'].transform(lambda x: ', '.join(x))
    return chunk.drop_duplicates(subset=['youtube_id', 'start_second', 'end_second'])

def merge_duplicates(input_path, output_path):
    # 定义块大小
    chunksize = 10000

    # 逐块处理文件并保存结果
    with pd.read_csv(input_path, names=column_names, header=None, chunksize=chunksize) as reader:
        total_rows = sum(1 for row in open(input_path, 'r'))
        with tqdm(total=total_rows) as pbar:
            for i, chunk in enumerate(reader):
                processed_chunk = process_chunk(chunk)
                if i == 0:
                    processed_chunk.to_csv(output_path, index=False, mode='w')
                else:
                    processed_chunk.to_csv(output_path, index=False, mode='a', header=False)
                pbar.update(len(chunk))
    print(f"处理完成，输出文件保存在 {output_path}")

def check_duplicates(csv_file_path, output_file_path):
    """检查 CSV 文件第一列元素是否有重复的行，并输出结果到文本文件"""
    # 读取 CSV 文件
    df = pd.read_csv(csv_file_path, names=column_names, header=None)
    
    # 检查第一列是否有重复值
    duplicates = df[df.duplicated(subset=df.columns[0], keep=False)]
    
    with open(output_file_path, 'w') as file:
        if not duplicates.empty:
            file.write("以下行在第一列有重复值：\n")
            file.write(duplicates.to_string(index=False))
            file.write("\n\n")
            
            # 统计每个重复值的重复次数
            duplicate_counts = df[df.duplicated(subset=df.columns[0], keep=False)][df.columns[0]].value_counts()
            file.write("重复的元素及其重复次数：\n")
            for item, count in duplicate_counts.items():
                file.write(f"{item}: {count} 次\n")
        else:
            file.write("没有找到重复的行。\n")
    print(f"检查完成，报告已输出到 {output_file_path}")

def main():
    # 先检查是否有重复行
    check_duplicates(file_path, report_path)
    
    # 然后合并重复行
    merge_duplicates(file_path, output_path)

if __name__ == "__main__":
    main()
