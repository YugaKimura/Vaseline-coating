import pandas as pd

def extract_cycle_time_columns(input_file, output_file):
    """
    指定したCSVファイルから、ヘッダーに "cycle time" を含む列のみを抽出し、新しいCSVに保存する。

    Parameters:
    ----------
    input_file : str
        入力CSVファイルのパス。
    output_file : str
        結果を保存するCSVファイルのパス。
    """
    try:
        # CSVを読み込む
        df = pd.read_csv(input_file)

        # "cycle time" を含む列のみ抽出（大文字小文字を無視）
        cycle_time_cols = [col for col in df.columns if "cycle length" in col.lower()]
        filtered_df = df[cycle_time_cols]

        # 結果を保存
        filtered_df.to_csv(output_file, index=False)
        print(f"Extracted columns saved to {output_file}")

    except Exception as e:
        print(f"Error processing file {input_file}: {e}")

# 使用例
input_file = "/home/erato_0/Documents/dlc/NewLabeling-Kimura-2024-12-26/kaiseki/hist.csv"  # 入力ファイルのパス
output_file = "/home/erato_0/Documents/dlc/NewLabeling-Kimura-2024-12-26/kaiseki/cdf/3/extracted_cycle_distance.csv"  # 結果を保存するファイル
extract_cycle_time_columns(input_file, output_file)
