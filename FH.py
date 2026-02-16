import pandas as pd
import os
import glob

def process_csv(file_path):
    """
    指定したCSVファイルからF列-H列（0ベースでは5-7）の結果を計算し、ファイル名と共に保存。

    Parameters:
    ----------
    file_path : str
        入力CSVファイルのパス。

    Returns:
    -------
    pd.DataFrame
        F列-H列の結果とファイル名を含むデータフレーム。
    """
    try:
        # CSVファイルを読み込む
        df = pd.read_csv(file_path, header=None,skiprows=1)  # 列名がない場合はheader=Noneを指定

        # 必要な列（インデックス5と7）が存在するか確認
        if df.shape[1] <= max(5, 7):
            print(f"Required columns missing in file: {file_path}")
            return None

        # F列 - H列（0ベースでは5 - 7）を計算
        df["F-H"] = df[5] - df[7]

        # ファイル名（セクション名）を取得
        section_name = os.path.splitext(os.path.basename(file_path))[0]

        # 結果をデータフレームとして返す
        return pd.DataFrame({
            "Section": [section_name] * len(df),
            "F-H": df["F-H"]
        })
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")
        return None

def process_all_files(input_dir, output_file):
    """
    フォルダ内のすべてのCSVファイルを処理し、F列-H列の結果をまとめて保存する。

    Parameters:
    ----------
    input_dir : str
        入力CSVファイルが保存されているフォルダ。
    output_file : str
        結果を保存するCSVファイルのパス。
    """
    all_data = []

    # 入力ディレクトリ内のすべてのCSVファイルを取得
    csv_files = glob.glob(os.path.join(input_dir, "*.csv"))

    for file_path in csv_files:
        # 各ファイルを処理して結果を取得
        df = process_csv(file_path)
        if df is not None:
            all_data.append(df)

    # 全てのデータを結合して保存
    if all_data:
        final_df = pd.concat(all_data, ignore_index=True)
        try:
            final_df.to_csv(output_file, index=False)
            print(f"Processed results saved to {output_file}")
        except Exception as e:
            print(f"Error saving file {output_file}: {e}")
    else:
        print("No valid data processed.")

# 使用例
input_dir = "/home/erato_0/Documents/dlc/NewLabeling-Kimura-2024-12-26/kaiseki/scatter/modify/cycle/processed/cut"  # 入力CSVファイルが保存されているフォルダ
output_file = "/home/erato_0/Documents/dlc/NewLabeling-Kimura-2024-12-26/kaiseki/scatter/modify/cycle/processed/cut/final_f_h_results.csv"  # 出力ファイルのパス
process_all_files(input_dir, output_file)
