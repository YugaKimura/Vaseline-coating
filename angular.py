import pandas as pd
import os
import glob

def process_csv(file_path):
    """
    指定したCSVファイルからAngular Velocity列を抽出し、ファイル名と共に返す。

    Parameters:
    ----------
    file_path : str
        入力CSVファイルのパス。

    Returns:
    -------
    pd.DataFrame
        ファイル名とAngular Velocity列のデータを含むデータフレーム。
    """
    try:
        # CSVファイルを読み込む
        df = pd.read_csv(file_path)

        # Angular Velocity列が存在するか確認
        if "Angular Velocity" not in df.columns:
            print(f"'Angular Velocity' column missing in file: {file_path}")
            return None

        # ファイル名（セクション名）を取得
        section_name = os.path.splitext(os.path.basename(file_path))[0]

        # Angular Velocity列を抽出し、セクション名を追加
        return pd.DataFrame({
            "Section": [section_name] * len(df),
            "Angular Velocity": df["Angular Velocity"]
        })
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")
        return None

def process_all_files(input_dir, landing_output, takeoff_output):
    """
    フォルダ内のすべてのCSVファイルを処理し、Angular Velocity列を
    landing用とtakeoff用で分けてまとめ、保存する。

    Parameters:
    ----------
    input_dir : str
        入力CSVファイルが保存されているフォルダ。
    landing_output : str
        landing用データを保存するCSVファイルのパス。
    takeoff_output : str
        takeoff用データを保存するCSVファイルのパス。
    """
    landing_data = []
    takeoff_data = []

    # 入力ディレクトリ内のすべてのCSVファイルを取得
    csv_files = glob.glob(os.path.join(input_dir, "*.csv"))

    for file_path in csv_files:
        # 各ファイルを処理して結果を取得
        df = process_csv(file_path)
        if df is not None:
            # ファイル名に基づいてデータを分類
            if "landing" in file_path.lower():
                landing_data.append(df)
            elif "takeoff" in file_path.lower():
                takeoff_data.append(df)

    # データを結合して保存
    if landing_data:
        final_landing_df = pd.concat(landing_data, ignore_index=True)
        try:
            final_landing_df.to_csv(landing_output, index=False)
            print(f"Landing results saved to {landing_output}")
        except Exception as e:
            print(f"Error saving file {landing_output}: {e}")
    else:
        print("No landing data processed.")

    if takeoff_data:
        final_takeoff_df = pd.concat(takeoff_data, ignore_index=True)
        try:
            final_takeoff_df.to_csv(takeoff_output, index=False)
            print(f"Takeoff results saved to {takeoff_output}")
        except Exception as e:
            print(f"Error saving file {takeoff_output}: {e}")
    else:
        print("No takeoff data processed.")

# 使用例
input_dir = "/home/erato_0/Documents/dlc/NewLabeling-Kimura-2024-12-26/kaiseki/scatter/modify/cycle/omega"  # 入力CSVファイルが保存されているフォルダ
landing_output = "/home/erato_0/Documents/dlc/NewLabeling-Kimura-2024-12-26/kaiseki/scatter/modify/cycle/omega/landing_angular_velocity.csv"  # landingデータの出力ファイル
takeoff_output = "/home/erato_0/Documents/dlc/NewLabeling-Kimura-2024-12-26/kaiseki/scatter/modify/cycle/omega/takeoff_angular_velocity.csv"  # takeoffデータの出力ファイル
process_all_files(input_dir, landing_output, takeoff_output)
