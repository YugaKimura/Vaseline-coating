import pandas as pd
import os
import glob

def remove_last_4_rows(input_file, output_dir):
    """
    CSVファイルの下4行を削除して新しいファイルに保存する。

    Parameters:
    ----------
    input_file : str
        入力CSVファイルのパス。
    output_dir : str
        出力ディレクトリ。
    """
    # CSVファイルを読み込む
    df = pd.read_csv(input_file, header=None)

    # 下4行を削除
    if len(df) > 4:
        df = df.iloc[:-4]

    # 保存先ファイル名の生成
    os.makedirs(output_dir, exist_ok=True)
    base_name = os.path.basename(input_file)
    output_file = os.path.join(output_dir, base_name)

    # 処理後のデータを保存
    df.to_csv(output_file, index=False, header=False)
    print(f"Processed file saved to {output_file}")

# 入力ディレクトリと出力ディレクトリ
input_dir = "/home/erato_0/Documents/dlc/NewLabeling-Kimura-2024-12-26/kaiseki/scatter/modify/cycle/processed"  # 処理対象のCSVファイルが入ったフォルダ
output_dir = "/home/erato_0/Documents/dlc/NewLabeling-Kimura-2024-12-26/kaiseki/scatter/modify/cycle/processed/cut"  # 処理後のCSVファイルを保存するフォルダ

# ディレクトリ内のすべてのCSVファイルを処理
csv_files = glob.glob(os.path.join(input_dir, "*.csv"))

for csv_file in csv_files:
    remove_last_4_rows(csv_file, output_dir)
