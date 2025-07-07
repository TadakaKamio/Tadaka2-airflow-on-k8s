import pandas as pd
import requests
from bs4 import BeautifulSoup


def fetch_tables_from_url(url):
    response = requests.get(url)
    if response.status_code != 200:
        print("Failed to retrieve data:", response.status_code)
        return []

    # HTML解析のための正しいエンコーディングを設定
    response.encoding = response.apparent_encoding

    # HTML解析
    soup = BeautifulSoup(response.text, "html.parser")

    # テーブルを見つける
    tables = soup.find_all("table")
    if not tables:
        print("No tables found on the page.")
        return []

    # 全てのテーブルをpandasのDataFrameに変換しリストで返す
    dfs = [pd.read_html(str(table))[0] for table in tables]
    return dfs


def flatten_columns(df):
    # マルチインデックス列をフラット化する
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = [" ".join(col).strip() for col in df.columns.values]
    return df


def save_dfs_to_excel(dfs, filename):
    with pd.ExcelWriter(filename, engine="openpyxl") as writer:
        for i, df in enumerate(dfs):
            sheet_name = f"Table {i + 1}"
            # 列をフラット化してからExcelに書き出す
            flatten_columns(df).to_excel(writer, sheet_name=sheet_name, index=False)


def save_all_dfs_to_one_sheet(dfs, filename):
    with pd.ExcelWriter(filename, engine="openpyxl") as writer:
        # すべてのDataFrameを結合する
        combined_df = pd.DataFrame()
        for df in dfs:
            # 列をフラット化
            flat_df = flatten_columns(df)
            # 現在のDataFrameを結合
            combined_df = pd.concat(
                [combined_df, flat_df, pd.DataFrame([[""] * len(flat_df.columns)])],
                ignore_index=True,
            )
        # Excelに書き出す
        combined_df.to_excel(writer, sheet_name="All Tables", index=False)


# URLを指定
url = (
    "https://www.enecho.meti.go.jp/category/electricity_and_gas/"
    "gas/liberalization/retailers_list/#ga01_b"
)

# テーブルを取得
dfs = fetch_tables_from_url(url)
if dfs:
    # Excelに保存
    # save_dfs_to_excel(dfs, r"C:\myProject\output_tables.xlsx")
    # print("All tables have been saved to 'output_tables.xlsx'.")

    save_all_dfs_to_one_sheet(dfs, r"C:\myProject\output_tables_all.xlsx")
    print("All tables have been saved to 'output_tables_all.xlsx'.")
