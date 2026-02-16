import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import ks_2samp, ttest_ind
import os
import glob

def get_common_name(file_path):
    """ ファイル名から共通部分を取得（拡張子を除いた部分） """
    return os.path.splitext(os.path.basename(file_path))[0]

def get_y_axis_limits(csv_files):
    """ 指定されたCSVファイル群のデータの範囲を取得し、y軸の最大値を統一（見切れ防止） """
    y_limits = {}

    for file_path in csv_files:
        common_name = get_common_name(file_path)

        try:
            df = pd.read_csv(file_path, header=None)
            if df.shape[1] < 3:
                print(f"File {file_path} does not have enough columns. Skipping.")
                continue

            col1, col2, col3 = df[0].dropna(), df[1].dropna(), df[2].dropna()
            min_val, max_val = min(col1.min(), col2.min(), col3.min()), max(col1.max(), col2.max(), col3.max())

            if common_name not in y_limits:
                y_limits[common_name] = [min_val, max_val]
            else:
                y_limits[common_name][0] = min(y_limits[common_name][0], min_val)
                y_limits[common_name][1] = max(y_limits[common_name][1], max_val)

        except Exception as e:
            print(f"Error processing file {file_path}: {e}")

    return y_limits

def plot_boxplot(file_path, output_dir, y_limits):
    """ Boxplotを作成し、保存する """
    try:
        df = pd.read_csv(file_path, header=None)

        if df.shape[1] < 3:
            print(f"File {file_path} does not have enough columns. Skipping.")
            return

        col1, col2, col3 = df[0].dropna(), df[1].dropna(), df[2].dropna()

        base_name = get_common_name(file_path)

        plt.figure(figsize=(8, 6))
        plt.boxplot([col1, col2, col3], labels=["pre", "propet", "post"])

        plt.rcParams["font.family"] = "Arial"
        plt.title(base_name, fontsize=16)
        plt.xlabel("", fontsize=13)
        plt.ylabel("Value", fontsize=13)

        if base_name in y_limits:
            y_min, y_max = y_limits[base_name]
            plt.ylim(min(0, y_min), y_max * 1.1)  # 1.1倍の余裕

        plt.grid(False)

        os.makedirs(output_dir, exist_ok=True)
        output_file = os.path.join(output_dir, f"{base_name}_boxplot.png")
        plt.savefig(output_file)
        plt.close()
        print(f"Boxplot saved to {output_file}")

    except Exception as e:
        print(f"Error processing file {file_path}: {e}")

def plot_cdf(file_path, output_dir):
    """ 累積確率分布曲線（CDF）を作成し、保存する """
    try:
        df = pd.read_csv(file_path, header=None)

        if df.shape[1] < 3:
            print(f"File {file_path} does not have enough columns. Skipping.")
            return

        col1, col2, col3 = df[0].dropna(), df[1].dropna(), df[2].dropna()

        base_name = get_common_name(file_path)

        plt.figure(figsize=(8, 6))
        for col, label in zip([col1, col2, col3], ["pre", "propet", "post"]):
            sorted_data = np.sort(col)
            cumulative = np.arange(1, len(sorted_data) + 1) / len(sorted_data)
            plt.plot(sorted_data, cumulative, label=label)

        plt.rcParams["font.family"] = "Arial"
        plt.title(base_name, fontsize=16)
        plt.xlabel("Value", fontsize=13)
        plt.ylabel("Cumulative Probability", fontsize=13)
        plt.legend(fontsize=12)

        plt.grid(False)

        os.makedirs(output_dir, exist_ok=True)
        output_file = os.path.join(output_dir, f"{base_name}_cdf.png")
        plt.savefig(output_file)
        plt.close()
        print(f"CDF plot saved to {output_file}")

    except Exception as e:
        print(f"Error processing file {file_path}: {e}")

def compute_p_values(file_path):
    """ KS検定 & Student's T検定のp値を計算し、辞書形式で返す """
    try:
        df = pd.read_csv(file_path, header=None)

        if df.shape[1] < 3:
            print(f"File {file_path} does not have enough columns. Skipping.")
            return None

        col1, col2, col3 = df[0].dropna(), df[1].dropna(), df[2].dropna()

        ks_p12, ks_p23, ks_p13 = ks_2samp(col1, col2).pvalue, ks_2samp(col2, col3).pvalue, ks_2samp(col1, col3).pvalue
        t_p12, t_p23, t_p13 = ttest_ind(col1, col2, equal_var=False).pvalue, ttest_ind(col2, col3, equal_var=False).pvalue, ttest_ind(col1, col3, equal_var=False).pvalue

        return {
            "Section": get_common_name(file_path),
            "KS pre-propet": ks_p12, "KS propet-post": ks_p23, "KS pre-post": ks_p13,
            "T pre-propet": t_p12, "T propet-post": t_p23, "T pre-post": t_p13
        }
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")
        return None

def process_all_files(input_dir, output_dir, output_p_values):
    """ フォルダ内のすべてのCSVファイルを処理してboxplot・CDFを作成し、p値を計算する """
    csv_files = glob.glob(os.path.join(input_dir, "*.csv"))
    y_limits = get_y_axis_limits(csv_files)

    p_values_results = []

    for file_path in csv_files:
        plot_boxplot(file_path, output_dir, y_limits)
        plot_cdf(file_path, output_dir)
        p_values = compute_p_values(file_path)
        if p_values:
            p_values_results.append(p_values)

    if p_values_results:
        pd.DataFrame(p_values_results).to_csv(output_p_values, index=False)
        print(f"P-values saved to {output_p_values}")

# 使用例
input_dir = "/home/erato_0/Documents/dlc/NewLabeling-Kimura-2024-12-26/kaiseki/cdf/3"
output_dir = "/home/erato_0/Documents/dlc/NewLabeling-Kimura-2024-12-26/kaiseki/cdf/3/moromoro"
output_p_values = "/home/erato_0/Documents/dlc/NewLabeling-Kimura-2024-12-26/kaiseki/cdf/3/moromoro/p_values_results.csv"
process_all_files(input_dir, output_dir, output_p_values)
