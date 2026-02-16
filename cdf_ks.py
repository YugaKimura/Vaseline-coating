import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import ks_2samp
import os

def process_csv(file_path, output_dir):
    """
    CSVファイルの0,1,2列目のデータから累積確率分布をプロットし、
    KS検定のp値を計算して保存する。

    Parameters:
    ----------
    file_path : str
        入力CSVファイルのパス。
    output_dir : str
        結果を保存するディレクトリ。
    """
    # CSVを読み込む
    try:
        df = pd.read_csv(file_path, header=None)
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return

    # 0,1,2列目のデータを取得
    try:
        col0 = df[0].dropna()
        col1 = df[1].dropna()
        #col2 = df[2].dropna()
    except KeyError as e:
        print(f"Required columns missing in file {file_path}: {e}")
        return

    # KS検定を実行
    ks_result_01 = ks_2samp(col0, col1)  # 列0 vs 列1
    #ks_result_02 = ks_2samp(col0, col2)  # 列0 vs 列2
    #ks_result_12 = ks_2samp(col1, col2)  # 列1 vs 列2

    # KS検定のp値
    p_value_01 = ks_result_01.pvalue
    #p_value_02 = ks_result_02.pvalue
    #p_value_12 = ks_result_12.pvalue

    # 累積確率分布のプロット
    plt.figure(figsize=(10, 6))
    for col, label in zip([col0, col1], ['without propet', 'propet']):
        sorted_data = np.sort(col)
        cumulative = np.arange(1, len(sorted_data) + 1) / len(sorted_data)
        plt.plot(sorted_data, cumulative, label=label)

    # グラフの設定
    plt.title("Stancemax Swingmin Time")
    plt.xlabel("Time [frames]")
    plt.ylabel("Cumulative Probability")
    plt.legend()
    plt.grid()

    # グラフを保存
    output_plot = os.path.join(output_dir, "Stm_Swm_1_cdf.png")
    os.makedirs(output_dir, exist_ok=True)
    plt.savefig(output_plot)
    plt.close()
    print(f"Cumulative distribution plot saved to {output_plot}")

    # KS検定結果を保存
    ks_results_file = os.path.join(output_dir, "ks_test_Stm_Swm_KS_KS.csv")
    ks_results = pd.DataFrame({
        "Comparison": ['without propet vs propet'],
        "KS Statistic": [ks_result_01.statistic],
        "p-value": [p_value_01]
    })
    ks_results.to_csv(ks_results_file, index=False)
    print(f"KS test results saved to {ks_results_file}")

# 使用例
input_csv = "/home/erato_0/Documents/dlc/NewLabeling-Kimura-2024-12-26/kaiseki/cdf/seisho/swing_duration_a.csv"  # 入力CSVファイルのパス
output_dir = "/home/erato_0/Documents/dlc/NewLabeling-Kimura-2024-12-26/kaiseki/cdf/seisho"  # 結果を保存するフォルダ
process_csv(input_csv, output_dir)
