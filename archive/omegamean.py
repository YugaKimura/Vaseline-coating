import pandas as pd
import numpy as np
import os
import glob

def calculate_mean_velocity_from_csv(file_path):
    """
    CSVファイルから角速度の平均を計算する。

    Parameters:
    ----------
    file_path : str
        入力CSVファイルのパス。

    Returns:
    -------
    float
        角速度の平均値。
    """
    try:
        # CSVファイルを読み込む
        df = pd.read_csv(file_path)
        if "Angular Velocity" in df.columns:
            return df["Angular Velocity"].mean()
        else:
            return np.nan
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")
        return np.nan

def process_all_means(input_dir, output_file):
    """
    フォルダ内のCSVファイルからLandingとTakeoffの角速度の平均値を計算し、
    指定の順番で1つのCSVファイルにまとめる。

    Parameters:
    ----------
    input_dir : str
        入力CSVファイルが保存されているフォルダ。
    output_file : str
        出力CSVファイルのパス。
    """
    # ファイル名の順番を定義
    order = [
        "rat8_1106", "rat9_1106", "rat10_1102", "rat10_1106", "rat11_1102", "rat11_1106"
    ]
    phases = ["pre", "propet", "post"]

    file_info = []
    landing_means = []
    takeoff_means = []

    for base in order:
        for phase in phases:
            # ファイルパスを生成
            landing_file = os.path.join(input_dir, f"{base}{phase}_3_landing_omega.csv")
            takeoff_file = os.path.join(input_dir, f"{base}{phase}_3_takeoff_omega.csv")

            # 各ファイルから平均角速度を計算
            landing_mean = calculate_mean_velocity_from_csv(landing_file)
            takeoff_mean = calculate_mean_velocity_from_csv(takeoff_file)

            # ファイル情報と平均値をリストに追加
            file_info.append(f"{base}_{phase}")
            landing_means.append(landing_mean)
            takeoff_means.append(takeoff_mean)

    # 結果をデータフレームにまとめる
    result_df = pd.DataFrame({
        "Source File": file_info,
        "Landing Mean Angular Velocity": landing_means,
        "Takeoff Mean Angular Velocity": takeoff_means
    })

    # CSVに保存
    result_df.to_csv(output_file, index=False)
    print(f"Saved mean velocities to {output_file}")

# 使用例
input_dir = "/home/erato_0/Documents/dlc/NewLabeling-Kimura-2024-12-26/kaiseki/scatter/modify/cycle/omega"  # 入力CSVファイルが保存されているフォルダ
output_file = "/home/erato_0/Documents/dlc/NewLabeling-Kimura-2024-12-26/kaiseki/scatter/modify/cycle/omega/omegamean.csv"  # 結果を保存するフォルダ
process_all_means(input_dir, output_file)
