import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
import numpy as np
df=pd.read_csv("1102propet_b_1.csv",header=None)
print(df)
stance=df[df[9]==1]
swing=df[df[9]==0]

t = df[0].values
#angle = df[7].values #all
#i_values = df[8].values #all
angle = df[8].values #pile
i_values = df[9].values #pile

# ポイント列をセグメントに変換
points = np.array([t, angle]).T.reshape(-1, 1, 2)
segments = np.concatenate([points[:-1], points[1:]], axis=1)

# セグメントごとに色を割り当て(stance=red,swing=blue)
seg_colors = []
for idx in range(len(segments)):
    if i_values[idx] == 1:
        seg_colors.append('red')
    else:
        seg_colors.append('blue')

lc = LineCollection(segments, colors=seg_colors, linewidths=0.25)

fig, ax = plt.subplots()
ax.add_collection(lc)
ax.set_xlim(np.nanmin(t),np.nanmax(t))
ax.set_ylim(np.nanmin(angle),np.nanmax(angle))
ax.set_title("1102propet")
ax.set_xlabel("Sec")
ax.set_ylabel("Angle")

plt.show()

#length = df[15].values #all
length = df[16].values #pile


# ポイント列をセグメントに変換
kon = np.array([t,length]).T.reshape(-1, 1, 2)
mascle = np.concatenate([kon[:-1], kon[1:]], axis=1)

# セグメントごとに色を割り当て
for idx in range(len(segments)):
    if i_values[idx] == 1:
        seg_colors.append('red')
    else:
        seg_colors.append('blue')

lc = LineCollection(mascle, colors=seg_colors, linewidths=0.25)

fig, ax = plt.subplots()
ax.add_collection(lc)
ax.set_xlim(0,1)
ax.set_ylim(0,300)
ax.set_title("906pre")
ax.set_xlabel("Sec")
ax.set_ylabel("Length")

plt.show()

