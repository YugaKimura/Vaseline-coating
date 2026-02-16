import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import glob

# color settings
blue = np.array([0, 128, 192]) / 256
navy_blue = np.array([0, 0, 100]) / 256

def get_common_name(file_path):
    """ ファイル名から共通部分を取得（拡張子を除いた部分） """
    return os.path.splitext(os.path.basename(file_path))[0]

def determine_labels_and_scaling(file_path, col1, col2):
    """ ファイル名に応じて適切なラベルを設定し、timeなら値を60で割る """
    file_name = os.path.basename(file_path).lower()

    if "time" in file_name:
        ylabel = "Time (s)"
        xlabel = "Time (s)"
        col1 /= 60  # 60で割る
        col2 /= 60
    elif "angle_1" in file_name:
        ylabel = "Angle (°)"
        xlabel = "Angle (°)"
    elif "velocity" in file_name:
        ylabel = "Angular Velocity (°/s)"
        xlabel = "Angular Velocity (°/s)"
    else:
        ylabel = "Value"
        xlabel = "Value"

    return ylabel, xlabel, col1, col2


def get_title_from_filename(file_path):
    """ ファイル名を適切なタイトル形式に変換 """
    file_name = os.path.basename(file_path).split('.')[0]  # 拡張子を除く
    title = file_name.replace('_', ' ')  # アンダースコアをスペースに変換
    title = title.title()  # 各単語の最初の文字を大文字に変換
    return title

def plot_boxplot_scatter(file_path, output_dir):
    """ BoxplotとScatterを重ねたプロットを作成し、保存する """
    try:
        df = pd.read_csv(file_path, header=None)
        if df.shape[1] < 2:
            print(f"File {file_path} does not have enough columns. Skipping.")
            return

        col1, col2 = df[0].dropna(), df[1].dropna()
        base_name = get_common_name(file_path)

        # ラベルとスケーリングを適用
        ylabel, _, col1, col2 = determine_labels_and_scaling(file_path, col1, col2)

        # グラフタイトルをファイル名から取得
        title = get_title_from_filename(file_path)

        # フォント設定
        plt.rcParams["font.family"] = "serif"       # 使用するフォント
        plt.rcParams["font.serif"] = "Arial"
        plt.rcParams['xtick.labelsize'] = 7 # 横軸のフォントサイズ（軸のみ変更）
        plt.rcParams['ytick.labelsize'] = 7 # 縦軸のフォントサイズ（軸のみ変更）
        plt.rcParams['font.size'] = 7 #フォントサイズを設定 default : 12

        # 軸設定
        plt.rcParams["figure.figsize"] = [30/25.4, 30/25.4] #??mm/25.4で書く（inch -> cm）
        plt.rcParams["xtick.major.size"] = 2.26772      # x軸主目盛り線の長さ(単位ポイント)
        plt.rcParams["ytick.major.size"] = 2.26772      # y軸主目盛り線の長さ
        plt.rcParams["xtick.major.width"] = 0.566929     # x軸主目盛り線の線幅
        plt.rcParams["ytick.major.width"] = 0.566929     # y軸主目盛り線の線幅
        plt.rcParams["axes.linewidth"] = 0.566929        # グラフ囲う線の太さ
        plt.rcParams['xtick.top'] = False  #x軸の上部目盛り
        plt.rcParams['ytick.right'] = False  #y軸の右部目盛り
        plt.rcParams["figure.dpi"] = 300            # dpi(dots per inch)
        # ラスタープロットの太さ
        plt.rcParams["lines.linewidth"] = 0.566929
        #ラスタープロットの長さ
        plt.rcParams["lines.markersize"] = 2.26772
        #スキャッタープロットなどの点の大きさ
        plt.rcParams["lines.markersize"] = 2.26772

        plt.figure(figsize=(8, 6))
        positions = [1, 2]

        # Boxplot（塗りつぶしなし）
        plt.boxplot([col1, col2], positions=positions, patch_artist=False, showfliers=False)
        
        # Scatterを重ねる
        for i, col in enumerate([col1, col2], start=1):
            plt.scatter([i] * len(col), col, alpha=0.6, color=blue if i == 1 else navy_blue)

        # グラフタイトルをファイル名から取得
        plt.title(title)
        plt.xticks([1, 2], ["baseline", "propet"])
        plt.ylabel(ylabel)

        plt.grid(False)

        os.makedirs(output_dir, exist_ok=True)
        output_file = os.path.join(output_dir, f"{base_name}_boxplot_scatter.png")
        plt.savefig(output_file)
        plt.close()
        print(f"Boxplot with Scatter saved to {output_file}")

    except Exception as e:
        print(f"Error processing file {file_path}: {e}")


def plot_cdf(file_path, output_dir):
    """ 累積確率分布曲線（CDF）を作成し、保存する """
    try:
        df = pd.read_csv(file_path, header=None)
        if df.shape[1] < 2:
            print(f"File {file_path} does not have enough columns. Skipping.")
            return

        col1, col2 = df[0].dropna(), df[1].dropna()
        base_name = get_common_name(file_path)

        # ラベルとスケーリングを適用
        _, xlabel, col1, col2 = determine_labels_and_scaling(file_path, col1, col2)

        # フォント設定
        # フォント設定
        plt.rcParams["font.family"] = "serif"       # 使用するフォント
        plt.rcParams["font.serif"] = "Arial"
        plt.rcParams['xtick.labelsize'] = 7 # 横軸のフォントサイズ（軸のみ変更）
        plt.rcParams['ytick.labelsize'] = 7 # 縦軸のフォントサイズ（軸のみ変更）
        plt.rcParams['font.size'] = 7 #フォントサイズを設定 default : 12

        # 軸設定
        plt.rcParams["figure.figsize"] = [30/25.4, 30/25.4] #??mm/25.4で書く（inch -> cm）
        plt.rcParams["xtick.major.size"] = 2.26772      # x軸主目盛り線の長さ(単位ポイント)
        plt.rcParams["ytick.major.size"] = 2.26772      # y軸主目盛り線の長さ
        plt.rcParams["xtick.major.width"] = 0.566929     # x軸主目盛り線の線幅
        plt.rcParams["ytick.major.width"] = 0.566929     # y軸主目盛り線の線幅
        plt.rcParams["axes.linewidth"] = 0.566929        # グラフ囲う線の太さ
        plt.rcParams['xtick.top'] = False  #x軸の上部目盛り
        plt.rcParams['ytick.right'] = False  #y軸の右部目盛り
        plt.rcParams["figure.dpi"] = 300            # dpi(dots per inch)
        # ラスタープロットの太さ
        plt.rcParams["lines.linewidth"] = 0.566929
        #ラスタープロットの長さ
        plt.rcParams["lines.markersize"] = 2.26772
        #スキャッタープロットなどの点の大きさ
        plt.rcParams["lines.markersize"] = 2.26772

        plt.figure(figsize=(8, 6))
        for col, label, color in zip([col1, col2], ["baseline", "propet"], [blue, navy_blue]):
            sorted_data = np.sort(col)
            cumulative = np.arange(1, len(sorted_data) + 1) / len(sorted_data)
            plt.plot(sorted_data, cumulative, label=label, color=color)

        plt.title(base_name)
        plt.xlabel(xlabel)
        plt.ylabel("Cumulative Probability")
        plt.legend()

        plt.grid(False)

        os.makedirs(output_dir, exist_ok=True)
        output_file = os.path.join(output_dir, f"{base_name}_cdf.png")
        plt.savefig(output_file)
        plt.close()
        print(f"CDF plot saved to {output_file}")

    except Exception as e:
        print(f"Error processing file {file_path}: {e}")

def process_all_files(input_dir, output_dir):
    """ 指定されたディレクトリ内のCSVファイルを処理し、グラフを作成 """
    csv_files = glob.glob(os.path.join(input_dir, "*.csv"))

    for file_path in csv_files:
        plot_boxplot_scatter(file_path, output_dir)
        plot_cdf(file_path, output_dir)

# データのあるディレクトリと出力先ディレクトリを指定
input_dir = "/home/erato_0/Documents/dlc/NewLabeling-Kimura-2024-12-26/kaiseki/cdf/seisho"  # 入力CSVファイルが保存されているフォルダ
output_dir = "/home/erato_0/Documents/dlc/NewLabeling-Kimura-2024-12-26/kaiseki/cdf/seisho/fig"  # グラフを保存するフォルダ
process_all_files(input_dir, output_dir)

