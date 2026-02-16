import pandas as pd
import os
import glob

def process_csv(file_path):
    """
    指定したCSVファイルからmin_zero_Index列のデータを抽出する。

    Parameters:
    ----------
    file_path : str
        入力CSVファイルのパス。

    Returns:
    -------
    pd.DataFrame
        ファイル名とmin_zero_Index列の値を持つデータフレーム。
    """
    try:
        # CSVファイルを読み込む
        df = pd.read_csv(file_path)

        # min_zero_Index列が存在するか確認
        if "last1-maxlast" not in df.columns:
            print(f"'min_zero_Index' column missing in file: {file_path}")
            return None

        # min_zero_Index列のデータを抽出
        min_zero_indices = df["last_Angle"].dropna().tolist()

        # ファイル名（セクション名）を取得
        section_name = os.path.splitext(os.path.basename(file_path))[0]

        # データフレームとして返す
        return pd.DataFrame({
            "Section": [section_name] * len(min_zero_indices),
            "last_Angle": min_zero_indices
        })
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")
        return None

def process_all_files(input_dir, output_file):
    """
    フォルダ内のすべてのCSVファイルを処理し、min_zero_Index列のデータを
    pre＆post（A列）とpropet（B列）にまとめて保存する。

    Parameters:
    ----------
    input_dir : str
        入力CSVファイルが保存されているフォルダ。
    output_file : str
        結果を保存するCSVファイルのパス。
    """
    # ファイル名の順番を定義
    order = [
        "rat8_1106", "rat9_1106", "rat10_1102", "rat10_1106", "rat11_1102", "rat11_1106"
    ]
    phases = ["pre", "propet"]
    #phases=["post"]

    all_data = []

    for base in order:
        for phase in phases:
            # ファイルパスを生成
            file_path = os.path.join(input_dir, f"{base}{phase}_3_processed.csv")

            # ファイルからデータを抽出
            df = process_csv(file_path)
            if df is not None:
                all_data.append(df)

    # 全てのデータを結合
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
output_file = "/home/erato_0/Documents/dlc/NewLabeling-Kimura-2024-12-26/kaiseki/scatter/modify/cycle/processed/cut/final_indices_landing_angle_1.csv"  # 出力ファイルのパス
process_all_files(input_dir, output_file)


#input_dir = "/home/erato_0/Documents/dlc/NewLabeling-Kimura-2024-12-26/kaiseki/scatter/modify/cycle/processed/cut"  # 入力CSVファイルが保存されているフォルダ
#output_file = "/home/erato_0/Documents/dlc/NewLabeling-Kimura-2024-12-26/kaiseki/scatter/modify/cycle/processed/cut/final_indices.csv"  # 出力ファイルのパス
#file_path = os.path.join(input_dir, f"{base}{phase}_3_processed.csv")