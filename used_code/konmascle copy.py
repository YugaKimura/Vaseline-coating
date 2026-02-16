import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
import numpy as np
df=pd.read_csv("1102propet_b_2.csv",header=None)
print(df)
stance=df[df[9]==1]
swing=df[df[9]==0]

t = df[0].values
#angle = df[7].values #all
#i_values = df[8].values #all
angle = df[8].values #pile
i_values = df[9].values #pile

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

# ポイント列をセグメントに変換
points = np.array([t, angle]).T.reshape(-1, 1, 2)
segments = np.concatenate([points[:-1], points[1:]], axis=1)

# セグメントごとに色を割り当て(stance=red,swing=blue)
seg_colors = []
for idx in range(len(segments)):
    if i_values[idx] == 1:
        seg_colors.append(red)
    else:
        seg_colors.append(green)

lc = LineCollection(segments, colors=seg_colors, linewidths=0.25)

fig, ax = plt.subplots()
ax.add_collection(lc)
#ax.plot(df[17],df[18]+df[19],color=purple) #a
#ax.plot(df[17],df[18]-df[19],color=purple) #a
#ax.plot(df[17],df[18],color=purple) #a
#ax.plot(df[17],df[20],color=light_blue) #a
#ax.plot(df[17],df[20]+df[21],color=light_blue) #a
#ax.plot(df[17],df[20]-df[21],color=light_blue) #a
ax.plot(df[18],df[19]+df[20],color=purple,) #b
ax.plot(df[18],df[19]-df[20],color=purple) #b
ax.plot(df[18],df[19],color=purple) #b
ax.plot(df[18],df[21],color=light_blue) #b
ax.plot(df[18],df[21]+df[22],color=light_blue) #b
ax.plot(df[18],df[21]-df[22],color=light_blue) #b
ax.set_xlim(0,1)
ax.set_ylim(np.nanmin(angle),np.nanmax(angle))
ax.set_xlabel("Sec")
ax.set_ylabel("Angle")
ax.set_title("1102propet")

plt.show()
