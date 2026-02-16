import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import os
import glob

# color settings
blue = np.array([0, 128, 192]) / 256
navy_blue = np.array([0, 0, 100]) / 256
purple  = np.array([200, 50, 255]) / 256

def get_common_name(file_path):
    """ ファイル名から共通部分を取得（拡張子を除いた部分） """
    return os.path.splitext(os.path.basename(file_path))[0]

def determine_labels_and_scaling(file_path, col1, col2):
    """ ファイル名に応じて適切なラベルを設定し、timeなら値を60で割る """
    file_name = os.path.basename(file_path).lower()

    if "duration" in file_name:
        ylabel = "Duration (s)"
        xlabel = "Duration (s)"
        col1 /= 60  # 60で割る
        col2 /= 60
    elif "angle" in file_name:
        ylabel = "Angle (deg)"
        xlabel = "Angle (deg)"
    elif "velocity" in file_name:
        ylabel = "Angular Velocity (°/s)"
        xlabel = "Angular Velocity (°/s)"
    elif "distance" in file_name:
        ylabel = "Distance (cm)"
        xlabel = "Distance (cm)"
        col1 *= 3/80  # 60で割る
        col2 *= 3/80
    else:
        ylabel = "Value"
        xlabel = "Value"

    return ylabel, xlabel, col1, col2


import os

def get_title_from_filename(file_path):
    # ファイル名部分（拡張子を除く）を取得
    file_name = os.path.basename(file_path).split('.')[0]
    
    # アンダースコアの前の部分だけ抽出
    # たとえば "cycle_duration" -> "cycle"
    first_part = file_name.split('_')[0]

    # 先頭を大文字、残りを小文字にする
    # "cycle" -> "Cycle"
    title = first_part.capitalize()
    
    return title

# 使用例:
# "cycle_duration.csv" -> "Cycle"
# "analysis_results.txt" -> "Analysis"
# "singleword.csv" -> "Singleword" (アンダースコアがなければそのまま先頭大文字化)


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
        plt.rcParams["figure.figsize"] = [50/25.4, 30/25.4] #??mm/25.4で書く（inch -> cm）
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
        plt.gca().spines["top"].set_visible(False)
        plt.gca().spines["left"].set_visible(False)
        plt.figure(figsize=(50/25.4,30/25.4),dpi=300)
        positions = [1, 2]

        # Boxplot（塗りつぶしなし）
        plt.boxplot([col1, col2], positions=positions, patch_artist=False, showfliers=False,medianprops=dict(color="black",linewidth=0.566929),
                    boxprops=dict(linewidth=0.566929),whiskerprops=dict(linewidth=0.566929),capprops=dict(linewidth=0.566929))
        
        # Scatterを重ねる
        for i, col in enumerate([col1, col2], start=1):
            plt.scatter([i] * len(col), col, alpha=0.6, edgecolors="black",facecolors="none",linewidth=0.566929)
        max_value = max(col1.max(), col2.max())
        current_ylim = plt.gca().get_ylim()  # 現在のy軸の範囲
        plt.ylim(current_ylim[0], max_value)
        # グラフタイトルをファイル名から取得
        plt.title(title)
        plt.xticks([1, 2], ["baseline", "propet"])
        plt.ylabel(ylabel,fontsize=8)

        plt.grid(False)
        plt.gca().spines["top"].set_visible(False)
        plt.gca().spines["right"].set_visible(False)
        os.makedirs(output_dir, exist_ok=True)
        output_file = os.path.join(output_dir, f"{base_name}_boxplot_scatter.tiff")
        plt.savefig(output_file,dpi=300,bbox_inches="tight")
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
        title = get_title_from_filename(file_path)

        # ラベルとスケーリングを適用
        _, xlabel, col1, col2 = determine_labels_and_scaling(file_path, col1, col2)

        # フォント設定
        plt.rcParams["font.family"] = "serif"       # 使用するフォント
        plt.rcParams["font.serif"] = "Arial"
        plt.rcParams['xtick.labelsize'] = 7 # 横軸のフォントサイズ（軸のみ変更）
        plt.rcParams['ytick.labelsize'] = 7 # 縦軸のフォントサイズ（軸のみ変更）
        plt.rcParams['font.size'] = 7 #フォントサイズを設定 default : 12

        # 軸設定
        plt.rcParams["figure.figsize"] = [50/25.4, 30/25.4] #??mm/25.4で書く（inch -> cm）
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

        # グラフ描画
        plt.figure(figsize=(50/25.4, 30/25.4), dpi=300)
        for col, label, color in zip([col1, col2], ["baseline", "propet"], ["black", purple]):
            sorted_data = np.sort(col)
            cumulative = np.arange(1, len(sorted_data) + 1) / len(sorted_data)
            plt.plot(sorted_data, cumulative, label=label, color=color)

            # 共通設定
            plt.ylim(0, 1)
            plt.yticks([0, 0.5, 1], ["0", " ", "1"], fontsize=8)
            plt.gca().spines["left"].set_position("zero")  # y軸を原点に配置
            plt.gca().spines["bottom"].set_position("zero")  # x軸を原点に配置
            plt.gca().xaxis.set_ticks_position("bottom")  # x軸の目盛り位置を下に
            plt.gca().yaxis.set_ticks_position("left")  # y軸の目盛り位置を左に

            # ファイルごとの個別設定
            if "_angle.csv" in os.path.basename(file_path):
                # "angle"がファイル名に含まれている場合
                xmin = np.min(col1)
                xmax = np.max(col1)
                second_tick = xmax - (xmax - xmin) * 0.05
                plt.xlim(55, 175)  # xmaxを少し広げる
                plt.xticks([50,100,150], fontsize=8)  # 2つのxticks
                plt.gca().spines["bottom"].set_position(("data",0)) # x軸を原点に配置
                plt.gca().spines["left"].set_position(("data",50))  # y軸を原点に配置
            elif "stance_duration_a.csv" in os.path.basename(file_path):
                # "duration_a.csv"の場合は通常設定
                plt.xlim(0, np.max(col1))
                plt.xticks([0, 0.5,1,1.5], fontsize=8)

            elif "swing_duration_a.csv" in os.path.basename(file_path):
                # "duration_a.csv"の場合は通常設定
                plt.xlim(0, np.max(col1))
                plt.xticks([0, 0.4,0.8], fontsize=8)

            elif "cycle_duration.csv" in os.path.basename(file_path):
                # "cycle_duration.csv"の場合は通常設定
                plt.xlim(0, np.max(col1))
                plt.xticks([0, 1,2], fontsize=8)



        # グラフの見た目設定
        plt.title(title)
        plt.xlabel(xlabel, fontsize=8)
        plt.ylabel("Cumulative probability", fontsize=8)
        plt.grid(False)
        plt.gca().spines["top"].set_visible(False)
        plt.gca().spines["right"].set_visible(False)

        os.makedirs(output_dir, exist_ok=True)
        output_file = os.path.join(output_dir, f"{base_name}_cdf.tiff")
        plt.savefig(output_file, dpi=300, bbox_inches="tight")
        plt.close()
        print(f"CDF plot saved to {output_file}")

    except Exception as e:
        print(f"Error processing file {file_path}: {e}")




def process_all_files(input_dir, output_dir):
    """ 指定されたディレクトリ内のCSVファイルを処理し、グラフを作成 """
    csv_files = glob.glob(os.path.join(input_dir, "*.csv"))

    for file_path in csv_files:
        #plot_boxplot_scatter(file_path, output_dir)
        plot_cdf(file_path, output_dir)

# データのあるディレクトリと出力先ディレクトリを指定
input_dir = "/home/erato_0/Documents/dlc/NewLabeling-Kimura-2024-12-26/kaiseki/cdf/seisho"  # 入力CSVファイルが保存されているフォルダ
output_dir = "/home/erato_0/Documents/dlc/NewLabeling-Kimura-2024-12-26/kaiseki/cdf/seisho/fig"  # グラフを保存するフォルダ
process_all_files(input_dir, output_dir)

#input_dir = "/home/erato_0/Documents/dlc/NewLabeling-Kimura-2024-12-26/kaiseki/cdf/seisho"  # 入力CSVファイルが保存されているフォルダ
#output_dir = "/home/erato_0/Documents/dlc/NewLabeling-Kimura-2024-12-26/kaiseki/cdf/seisho/fig"  # グラフを保存するフォルダ
