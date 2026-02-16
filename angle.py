import pandas as pd
import numpy as np
import glob
import os

def calculate_angle(wrist, elbow, shoulder, degrees=True):
    """
    三点 (wrist, elbow, shoulder) から肘 (elbow) を頂点とする角度を計算する。

    Parameters:
    -----------
    wrist : tuple or list
        (x, y) 座標
    elbow : tuple or list
        (x, y) 座標
    shoulder : tuple or list
        (x, y) 座標
    degrees : bool
        True の場合、角度を度数法で返す。False の場合、ラジアンで返す。

    Returns:
    --------
    float
        計算された角度
    """
    A = np.array(wrist, dtype=float)
    B = np.array(elbow, dtype=float)
    C = np.array(shoulder, dtype=float)

    BA = A - B
    BC = C - B

    dot_product = np.dot(BA, BC)
    norm_BA = np.linalg.norm(BA)
    norm_BC = np.linalg.norm(BC)

    if norm_BA == 0 or norm_BC == 0:
        return np.nan  # ベクトルの長さが0の場合はNaNを返す

    cos_theta = dot_product / (norm_BA * norm_BC)
    cos_theta = np.clip(cos_theta, -1.0, 1.0)  # 数値誤差対策
    theta = np.arccos(cos_theta)

    if degrees:
        theta = np.degrees(theta)

    return theta

# CSV ファイルが保存されているディレクトリのパス
input_dir ='/home/erato_0/Documents/dlc/NewLabeling-Kimura-2024-12-26/kaiseki/scatter/modify'  # ここを実際のパスに変更してください

# 指定ディレクトリ内の全ての CSV ファイルを取得
csv_files = glob.glob(os.path.join(input_dir, '*.csv'))

for file_path in csv_files:
    print(f"Processing: {file_path}")
    
    # ヘッダーがないと仮定して読み込む
    df = pd.read_csv(file_path, header=None)
    
    # 列数を確認（最低限6列必要）
    if df.shape[1] < 6:
        print(f"Error: {file_path} has fewer than 6 columns. Skipping.")
        continue
    
    # wrist: 列 0 (x), 列 1 (y)
    # elbow: 列 2 (x), 列 3 (y)
    # shoulder: 列 4 (x), 列 5 (y)
    
    # 角度を計算
    angles = df.apply(lambda row: calculate_angle(
        (row[0], row[1]),  # wrist
        (row[2], row[3]),  # elbow (頂点)
        (row[4], row[5]),  # shoulder
        degrees=True
    ), axis=1)
    
    # I列 (列インデックス8) に角度を追加
    # 既にG,H列（6,7）が埋まっているので、I列は8
    if df.shape[1] > 8:
        df.iloc[:, 8] = angles
    else:
        # 必要な列まで拡張
        for i in range(df.shape[1], 8):
            df[i] = np.nan
        df[8] = angles
    
    # 出力ファイル名を作成（例: "data.csv" → "data_with_angle.csv"）
    base_name = os.path.splitext(os.path.basename(file_path))[0]
    new_file_name = f"{base_name}_with_angle.csv"
    output_path = os.path.join(input_dir, new_file_name)
    
    # CSV を保存（ヘッダーなし、インデックスなし）
    df.to_csv(output_path, index=False, header=False)
    print(f"Saved to: {output_path}\n")

print("All files processed successfully.")
