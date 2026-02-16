import pandas as pd
import numpy as np
import glob
import os

def process_csv(file_path):
    # ヘッダーなしで読み込む
    df = pd.read_csv(file_path, header=None)
    
    # 列数確認（最低限 H 列 (列インデックス 7) 必要）
    if df.shape[1] < 8:
        print(f"Error: {file_path} has fewer than 8 columns. Skipping.")
        return None
    
    # K列 (列インデックス 10)
    K = [1]  # K1 は 1
    for i in range(1, len(df)):
        if df.iloc[i - 1, 7] == 0 and (i < len(df) - 1 and df.iloc[i, 7] == 1):
            K.append(1)
        else:
            K.append(K[-1] + 1 if i > 0 else 1)
    
    # L列 (列インデックス 11)
    L = []
    for i in range(len(K)):
        if i < len(K) - 1 and K[i + 1] == 1:
            L.append(K[i])
        else:
            L.append(" ")
    
    # M列 (列インデックス 12)
    M = [1]  # M1 は 1
    for i in range(1, len(df)):
        if df.iloc[i, 7] != df.iloc[i - 1, 7]:
            M.append(1)
        else:
            M.append(M[-1] + 1 if i > 0 else 1)
    
    # N列 (列インデックス 13)
    N = []
    for i in range(len(M)):
        if i < len(M) - 1 and M[i + 1] == 1:
            N.append(M[i])
        else:
            N.append(" ")
    
    # 新しい列を DataFrame に追加
    df[10] = K  # K列
    df[11] = L  # L列
    df[12] = M  # M列
    df[13] = N  # N列
    
    return df

# CSV ファイルが保存されているディレクトリのパス
input_dir = '/home/erato_0/Documents/dlc/NewLabeling-Kimura-2024-12-26/kaiseki/scatter/modify/cycle/nye'  # 実際のパスに変更
output_dir ='/home/erato_0/Documents/dlc/NewLabeling-Kimura-2024-12-26/kaiseki/scatter/modify/cycle'  # 出力用ディレクトリを指定
os.makedirs(output_dir, exist_ok=True)

# 指定ディレクトリ内の全ての CSV ファイルを取得
csv_files = glob.glob(os.path.join(input_dir, '*.csv'))

for file_path in csv_files:
    print(f"Processing: {file_path}")
    processed_df = process_csv(file_path)
    if processed_df is not None:
        # 出力ファイル名を作成（例: "data.csv" → "data_processed.csv"）
        base_name = os.path.splitext(os.path.basename(file_path))[0]
        new_file_name = f"{base_name}_processed.csv"
        output_path = os.path.join(output_dir, new_file_name)
        
        # CSV を保存（ヘッダーなし、インデックスなし）
        processed_df.to_csv(output_path, index=False, header=False)
        print(f"Saved to: {output_path}\n")

print("All files processed successfully.")
