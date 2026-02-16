import pandas as pd
import glob
import os

# CSV ファイルが入っているディレクトリのパス
input_dir = '/home/erato_0/Documents/dlc/NewLabeling-Kimura-2024-12-26/kaiseki/scatter/modify'

# 18 枚の csv ファイルをまとめて取得
csv_files = glob.glob(os.path.join(input_dir, "*.csv"))

for file_path in csv_files:
    print(f"Processing: {file_path}")
    
    # ヘッダーがないと仮定 -> header=None で読み込む
    df = pd.read_csv(file_path, header=None)

    # 列 7, 9, 11 を -1 倍する
    # （ファイルによっては列が不足する場合もあるので、index 範囲チェックしておくと安心）
    for col_idx in [7, 9, 11]:
        if col_idx < df.shape[1]:
            df.iloc[:, col_idx] = df.iloc[:, col_idx] * -1

    # 列 0~5 (6 列ぶん) を削除
    # たとえば、列数が 12 以上あることを前提にすると下記で OK
    # (あるいは df.shape[1] > 6 のときだけ削除する、などエラー回避するなら要チェック)
    df.drop(df.columns[0:6], axis=1, inplace=True)

    # 出力ファイル名: 元のファイル名 + "_modified.csv"
    base, ext = os.path.splitext(os.path.basename(file_path))
    output_file = os.path.join(input_dir, f"{base}_modified.csv")

    # ヘッダー行も不要なら header=False で出力
    df.to_csv(output_file, index=False, header=False)
    print(f"Saved to {output_file}")