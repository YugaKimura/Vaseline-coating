import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import random

A = pd.read_csv("/home/erato_0/Documents/dlc/NewLabeling-Kimura-2024-12-26/kaiseki/scatter/modify/cycle/rat10_1106pre_3.csv", header=None)

plt.rcParams["font.family"] = "serif"  # 使用するフォント
plt.rcParams["font.serif"] = "Arial"
plt.rcParams['xtick.labelsize'] = 7  # 横軸のフォントサイズ（軸のみ変更）
plt.rcParams['ytick.labelsize'] = 7  # 縦軸のフォントサイズ（軸のみ変更）
plt.rcParams['font.size'] = 7  # フォントサイズを設定 default : 12

# 軸設定
plt.rcParams["figure.figsize"] = [50 / 25.4, 30 / 25.4]  # mm/25.4で書く（inch -> cm）
plt.rcParams["xtick.major.size"] = 2.26772  # x軸主目盛り線の長さ(単位ポイント)
plt.rcParams["ytick.major.size"] = 2.26772  # y軸主目盛り線の長さ
plt.rcParams["xtick.major.width"] = 0.566929  # x軸主目盛り線の線幅
plt.rcParams["ytick.major.width"] = 0.566929  # y軸主目盛り線の線幅
plt.rcParams["axes.linewidth"] = 0.566929  # グラフ囲う線の太さ
plt.rcParams['xtick.top'] = False  # x軸の上部目盛り
plt.rcParams['ytick.right'] = False  # y軸の右部目盛り
plt.rcParams["figure.dpi"] = 300  # dpi(dots per inch)
# ラスタープロットの太さ
plt.rcParams["lines.linewidth"] = 0.566929
# ラスタープロットの長さ
plt.rcParams["lines.markersize"] = 2.26772
# スキャッタープロットなどの点の大きさ
plt.rcParams["lines.markersize"] = 2.26772

blue = np.array([0, 128, 192]) / 256
green = np.array([20, 180, 20]) / 256
purple = np.array([200, 50, 255]) / 256

# サイクルごとにデータを分割（空白行で区切る）
cycles = []
current_cycle = []

for i in range(len(A)):
    if pd.isna(A.iloc[i, 0]):  # 空白行を見つけたら
        if current_cycle:  # 現在のサイクルがあれば保存
            cycles.append(np.array(current_cycle))
        current_cycle = []  # 新しいサイクルを開始
    else:
        current_cycle.append(A.iloc[i])

# 最後のサイクルも保存
if current_cycle:
    cycles.append(np.array(current_cycle))

# 連続した10サイクルをランダムに選択
random_start = random.randint(0, len(cycles) - 11)  # 連続した10サイクルを選ぶため、範囲を制限
selected_cycles = cycles[random_start: random_start + 10]

# 選んだサイクルを連続して描画
for cycle in selected_cycles:
    # x, y 値の取得
    x = (cycle[:, 1]-300) * 3 / 80
    y = (cycle[:, 2]+300) * 3 / 80
    a=(cycle[:,3]-300)*3/80
    b=(cycle[:,4]+300)*3/80
    c=(cycle[:,5]-300)*3/80
    d=(cycle[:,6]+300)*3/80
    # サイクルをプロット
    plt.plot(x, y, color=blue, marker=None)
    plt.plot(a, b, color=green, marker=None)
    plt.scatter(c, d, color="white",edgecolors="black",marker=None,linewidths=0.566929)

# 軸設定
plt.xlim(-100 * 3 / 80, 200 * 3 / 80)
plt.xlabel('x (cm)', fontsize=8)
plt.xticks(np.arange(-6,7,6))
plt.ylim(-150 * 3 / 80, 200 * 3 / 80)
plt.yticks(np.arange(-6,7,6))
plt.ylabel('y (cm)', fontsize=8)
plt.title("Baseline")

# 軸の目盛り線とタイトルの設定
plt.gca().spines["top"].set_visible(False)
plt.gca().spines["right"].set_visible(False)

# 描画
#plt.show()


plt.savefig("/home/erato_0/Documents/dlc/NewLabeling-Kimura-2024-12-26/kaiseki/cdf/seisho/fig/Pre_plot.tiff",dpi=300,bbox_inches="tight")
plt.close()
#plt.show()
