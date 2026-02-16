import pandas as pd
import glob
import os

# 指定ディレクトリ内のすべてのCSVファイルを取得
input_dir = '/home/erato_0/Documents/dlc/NewLabeling-Kimura-2024-12-26/kaiseki/scatter/modify/cycle'  # CSVファイルが保存されているディレクトリのパス
output_dir = '/home/erato_0/Documents/dlc/NewLabeling-Kimura-2024-12-26/kaiseki/scatter/modify/cycle'  # 出力用ディレクトリ
os.makedirs(output_dir, exist_ok=True)  # 出力用ディレクトリがなければ作成

csv_files = glob.glob(os.path.join(input_dir, '*.csv'))

for file_path in csv_files:
    print(f"Processing: {file_path}")
    
    # CSVを読み込む（ヘッダーなし、0ベースのインデックスで処理）
    df = pd.read_csv(file_path, header=None)
    
    # L列（旧K列: インデックス10）をもとに計算
    l_col_index = 10  # L列 (0ベースインデックス)
    if l_col_index >= df.shape[1]:
        print(f"Error: L列(インデックス{l_col_index}）が存在しません。スキップします。")
        continue

    # 新しいA列を作成（L列を-1して60で割る計算結果を追加）
    df.insert(0, 'A', (df.iloc[:, l_col_index] - 1) / 60)

    # 出力ファイル名を作成（例: "data.csv" → "data_with_a_column.csv"）
    base_name = os.path.splitext(os.path.basename(file_path))[0]
    new_file_name = f"{base_name}_with_a_column.csv"
    output_path = os.path.join(output_dir, new_file_name)

    # CSVを保存（ヘッダーなし、インデックスなし）
    df.to_csv(output_path, index=False, header=False)
    print(f"Saved to: {output_path}\n")

print("All files processed successfully.")


