import pandas as pd
import numpy as np
import glob
import os

def calculate_distance(coord1, coord2):
    """
    2点間のユークリッド距離を計算する関数。

    Parameters:
    -----------
    coord1 : tuple or list
        (x, y) 座標
    coord2 : tuple or list
        (x, y) 座標

    Returns:
    --------
    float
        2点間の距離
    """
    return np.sqrt((coord1[0] - coord2[0])**2 + (coord1[1] - coord2[1])**2)

# CSV ファイルが保存されているディレクトリのパス
input_dir = '/home/erato_0/Documents/dlc/NewLabeling-Kimura-2024-12-26/kaiseki/scatter/modify'  # ここを実際のパスに変更してください

# 指定ディレクトリ内の全ての CSV ファイルを取得
csv_files = glob.glob(os.path.join(input_dir, '*.csv'))

for file_path in csv_files:
    print(f"Processing: {file_path}")
    
    # ヘッダーがないと仮定して読み込む
    df = pd.read_csv(file_path, header=None)
    
    # 列数を確認（最低限2列必要: A (x), B (y)）
    if df.shape[1] < 2:
        print(f"Error: {file_path} has fewer than 2 columns. Skipping.")
        continue
    
    # 手首 (wrist) の座標を取得 (A列: x, B列: y)
    wrist_coords = df.iloc[:, [0, 1]].values  # (x, y) の2次元配列を取得
    
    # 移動距離を計算
    distances = [0.0]  # J1 (最初の距離) は 0
    for i in range(1, len(wrist_coords)):
        dist = calculate_distance(wrist_coords[i - 1], wrist_coords[i])
        distances.append(dist)
    
    # J列 (列インデックス9) に移動距離を追加
    # 既にJ列が存在する場合は上書き、新規の場合は追加
    if df.shape[1] > 9:
        df.iloc[:, 9] = distances
    else:
        for i in range(df.shape[1], 9):
            df[i] = np.nan  # 必要な列まで埋める
        df[9] = distances
    
    # 出力ファイル名を作成（例: "data.csv" → "data_with_distance.csv"）
    base_name = os.path.splitext(os.path.basename(file_path))[0]
    new_file_name = f"{base_name}_with_distance.csv"
    output_path = os.path.join(input_dir, new_file_name)
    
    # CSV を保存（ヘッダーなし、インデックスなし）
    df.to_csv(output_path, index=False, header=False)
    print(f"Saved to: {output_path}\n")

print("All files processed successfully.")
