import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
a=pd.read_csv("hist.csv",header=None)
#print(a)
bin_edges = np.arange(0,201, 20)  # 0,10,20,...,100

# フォント設定
plt.rcParams["font.family"] = "serif"       # 使用するフォント
plt.rcParams["font.serif"] = "Arial"
plt.rcParams['xtick.labelsize'] = 7 # 横軸のフォントサイズ（軸のみ変更）
plt.rcParams['ytick.labelsize'] = 7 # 縦軸のフォントサイズ（軸のみ変更）
plt.rcParams['font.size'] = 7 #フォントサイズを設定 default : 12

# 軸設定
#plt.rcParams["figure.figsize"] = [30/25.4, 30/25.4] #??mm/25.4で書く（inch -> cm）
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

# color
blue =  np.array([0, 128, 192]) / 256
red = np.array([255, 70, 50]) / 256
pink = np.array([255, 150, 200]) / 256
green = np.array([20, 180, 20]) / 256
yellow = np.array([230, 160, 20]) / 256
gray = np.array([128, 128, 128]) / 256
purple  = np.array([200, 50, 255]) / 256
light_blue = np.array([20, 200, 200]) / 256
brown  = np.array([128, 0, 0]) / 256
navy_blue  = np.array([0, 0, 100]) / 256
vermilion  = np.array([228, 94, 50]) / 256

a806=0
a906=a806+18
a1002=a906+18
a1006=a1002+18
a1102=a1006+18
a1106=a1102+18

# ヒストグラム描画
plt.hist(a[a806], alpha=0.5,bins=bin_edges, color=green, label='pre')
plt.hist(a[a806+6], alpha=0.5, bins=bin_edges,color=purple, label='propet')
plt.hist(a[a806+12], alpha=0.5, bins=bin_edges,color=navy_blue, label='post')
#1002:+18  1102:+36
# Data1の中央値
median1 = a[a806].median()
print(median1)
plt.axvline(median1, color=green, linewidth=1, label='Median pre',zorder=3)

# Data2の中央値
median2 = a[a806+6].median()
plt.axvline(median2, color=purple, linewidth=1, label='Median propet',zorder=3)

median3 = a[a806+12].median()
plt.axvline(median3, color=navy_blue, linewidth=1, label='Median post',zorder=3)

# 軸ラベルやタイトル、凡例
plt.xlabel('Time')
plt.ylabel('Frequency')
plt.title('rat8 cycle time')
plt.legend()

plt.show()
