import pandas as pd
import matplotlib.pyplot as plt
import os
import glob

def get_common_name(file_path):
    """
    ファイル名から共通部分を取得（_KS または _1 の前まで）

    Parameters:
    ----------
    file_path : str
        CSVファイルのパス

    Returns:
    -------
    str
        ファイルの共通部分の名前
    """
    base_name = os.path.basename(file_path)
    return base_name.rsplit("_", 1)[0]  # "_1" または "_KS" の前の部分を返す

def get_y_axis_limits(csv_files):
    """
    指定されたCSVファイル群のデータの範囲を取得し、y軸の最大値を統一（大きい方に合わせる）。

    Parameters:
    ----------
    csv_files : list
        CSVファイルのパスのリスト

    Returns:
    -------
    dict
        各共通ファイル名ごとのy軸の最小値と最大値（見切れ防止のため余裕を持たせる）
    """
    y_limits = {}

    for file_path in csv_files:
        common_name = get_common_name(file_path)

        try:
            df = pd.read_csv(file_path, header=None)
            if df.shape[1] < 2:
                print(f"File {file_path} does not have enough columns. Skipping.")
                continue

            # 1列目と2列目のデータを取得
            col1 = df[0].dropna()
            col2 = df[1].dropna()

            min_val = min(col1.min(), col2.min())
            max_val = max(col1.max(), col2.max())

            if common_name not in y_limits:
                y_limits[common_name] = [min_val, max_val]
            else:
                y_limits[common_name][0] = min(y_limits[common_name][0], min_val)
                y_limits[common_name][1] = max(y_limits[common_name][1], max_val)

        except Exception as e:
            print(f"Error processing file {file_path}: {e}")

    return y_limits

def plot_boxplot(file_path, output_dir, y_limits):
    """
    指定したCSVファイルの1列目と2列目のデータを用いてboxplotを作成し、出力する。

    Parameters:
    ----------
    file_path : str
        入力CSVファイルのパス。
    output_dir : str
        グラフを保存するディレクトリ。
    y_limits : dict
        各共通名に対するy軸の最小・最大値を格納する辞書
    """
    try:
        # CSVファイルを読み込む
        df = pd.read_csv(file_path, header=None)

        # 必要な列が存在するか確認
        if df.shape[1] < 2:
            print(f"File {file_path} does not have enough columns. Skipping.")
            return

        # 1列目と2列目のデータを取得
        col1 = df[0].dropna()
        col2 = df[1].dropna()

        # ファイル名を取得
        base_name = os.path.basename(file_path)
        title_part = get_common_name(file_path)

        # x軸ラベルと出力ファイル名を決定
        if base_name.endswith("_1.csv"):
            labels = ["pre", "propet"]
            output_filename = f"{title_part}_prepropet.png"
        elif base_name.endswith("_KS.csv"):
            labels = ["not propet", "propet"]
            output_filename = f"{title_part}_nopropet.png"
        else:
            print(f"Skipping file {file_path} due to unknown naming pattern.")
            return

        # Boxplotを作成
        plt.figure(figsize=(8, 6))
        plt.boxplot([col1, col2], labels=labels)

        # フォント設定
        plt.rcParams["font.family"] = "Arial"

        # タイトルとラベルのサイズを1.3倍に設定
        plt.title(title_part, fontsize=16)  # デフォルト12 × 1.3
        plt.xlabel("", fontsize=13)  # デフォルト10 × 1.3
        plt.ylabel("Value", fontsize=13)  # デフォルト10 × 1.3

        # y軸の最大値を統一し、見切れを防ぐ（余裕を持たせる）
        if title_part in y_limits:
            y_min, y_max = y_limits[title_part]
            plt.ylim(min(0, y_min), y_max * 1.1)  # 最大値の1.1倍で設定

        # 中目盛り線を削除
        plt.grid(False)

        # 保存
        os.makedirs(output_dir, exist_ok=True)
        output_file = os.path.join(output_dir, output_filename)
        plt.savefig(output_file)
        plt.close()
        print(f"Boxplot saved to {output_file}")

    except Exception as e:
        print(f"Error processing file {file_path}: {e}")

def process_all_files(input_dir, output_dir):
    """
    フォルダ内のすべてのCSVファイルを処理し、1列目と2列目のboxplotを作成して保存する。
    同じ共通名のグラフはy軸の最大値を統一し、見切れが発生しないようにする。

    Parameters:
    ----------
    input_dir : str
        入力CSVファイルが保存されているフォルダ。
    output_dir : str
        グラフを保存するディレクトリ。
    """
    # 入力ディレクトリ内のすべてのCSVファイルを取得
    csv_files = glob.glob(os.path.join(input_dir, "*.csv"))

    # 各共通名ごとのy軸の最大値を取得（見切れを防ぐため余裕を持たせる）
    y_limits = get_y_axis_limits(csv_files)

    for file_path in csv_files:
        try:
            plot_boxplot(file_path, output_dir, y_limits)
        except Exception as e:
            print(f"Error processing file {file_path}: {e}")

# 使用例
input_dir = "/home/erato_0/Documents/dlc/NewLabeling-Kimura-2024-12-26/kaiseki/cdf/boxplot"  # 入力CSVファイルが保存されているフォルダ
output_dir = "/home/erato_0/Documents/dlc/NewLabeling-Kimura-2024-12-26/kaiseki/cdf/boxplot"  # グラフを保存するフォルダ
process_all_files(input_dir, output_dir)



#input_dir = "/home/erato_0/Documents/dlc/NewLabeling-Kimura-2024-12-26/kaiseki/cdf/boxplot"  # 入力CSVファイルが保存されているフォルダ
#output_dir = "/home/erato_0/Documents/dlc/NewLabeling-Kimura-2024-12-26/kaiseki/cdf/boxplot"  # グラフを保存するフォルダ
