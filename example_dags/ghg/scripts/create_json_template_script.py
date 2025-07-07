import json
import math
import unicodedata

import pandas as pd

import ghg.common.settings as Constants
import ghg.common.settings_shitei_info as SiteiInfoConstants
import ghg.common.settings_tokutei_info as TokuteiInfoConstants
from ghg.common.log import MyAppLog, log_writer

logger = MyAppLog()


# Excelのデータを基にJSON構造を作成する関数
@log_writer(logger)
def create_json_template(df, keyName):
    json_template = {}

    # 階層レベルに基づいてキーを構築するための一時的な辞書
    level_keys = {0: keyName}

    # C列～L列の範囲を選択
    item_name_columns = df.iloc[:, 2:11]
    other_columns = df.drop(df.columns[2:11], axis=1)
    # NaN値を空の文字列で置換する
    other_columns.fillna("", inplace=True)
    # 処理した結果を結合する
    df = pd.concat(
        [other_columns.iloc[:, :2], item_name_columns, other_columns.iloc[:, 2:]],
        axis=1,
    )

    # 各行に対して処理
    for _, row in df.iterrows():
        no = str(row.iloc[0])  # A列: 項番
        key = row.iloc[20]  # U列: タグ名
        # unique_key = f"{no}_{key}"  # キー名の一意性を確保
        level = convert_fullnumber_to_halfnumber(row.iloc[1])  # B列: レベル
        min_loops = convert_fullnumber_to_halfnumber(row.iloc[12])  # M列: 最小回数
        max_loops = convert_fullnumber_to_halfnumber(row.iloc[13])  # N列: 最大回数
        required = convert_required_symbol(row.iloc[14])  # O列: 必須
        value_type = row.iloc[15]  # P列: 値の型
        max_length = row.iloc[16]  # Q列: 最大文字数
        value_range = row.iloc[17]  # R列: データ範囲
        rounding_digit = convert_float_to_int(row.iloc[24])  # Y列: 小数第N位を四捨五入
        item_name = next(
            (value for value in row[2:11] if pd.notna(value)), ""
        )  # C列～L列: 項目名

        # 階層レベルに応じたキーの更新
        level_keys[level] = key

        # 親キーの構築
        parent_keys = [level_keys[lvl] for lvl in range(1, level)]
        unique_key = "$".join(parent_keys + [key])

        # JSONキーの構築
        json_key_info = {
            "no": no,
            "level": level,
            "key": key,
            "item_name": item_name,
            "minOccurs": min_loops,
            "maxOccurs": max_loops,
            "required": required,
            "type": value_type,
            "maxLength": max_length,
            "valueRange": value_range,
            "rounding_digit": rounding_digit,
        }

        # 階層に基づいてキーを辞書に追加
        json_template[unique_key] = json_key_info

    return json_template


# データの変換処理関数
@log_writer(logger)
def convert_float_to_int(value):
    # 値が None、NaN、空文字列でない場合に int に変換
    if (
        value is not None
        and value != ""
        and not math.isnan(value)
        and isinstance(value, float)
    ):
        return int(value)
    else:
        return value


@log_writer(logger)
def convert_fullnumber_to_halfnumber(value):
    if isinstance(value, str):
        # 全角数字を半角数字に変換
        value = unicodedata.normalize("NFKC", value)
        # 文字列を数字に変換
        value = int(value)
    return value


@log_writer(logger)
def convert_required_symbol(value):
    if isinstance(value, str):
        # 必須項目の記号を統一
        value = value.replace("〇", "○")
    return value


def create_shitei_info_json(**kwargs):
    # pandasを使用してExcelファイルを読み込む
    df = pd.read_excel(
        Constants.FOLDER_PATH_XML_TEMPLETE,
        sheet_name="XML構造設計書（様式第9）指定表",
        skiprows=8,
        nrows=1399,  # 第10行から第1408行まで読み込む
        usecols="A:Y",  # A列からY列まで読み込む
        engine=Constants.PackageName.PANDAS_ENGINE.value,
    )
    json_template = create_json_template(df, "Shiteihyo")

    # JSONテンプレートを出力
    json_output = json.dumps(json_template, indent=4, ensure_ascii=False)

    # JSONファイルに出力
    with open(
        SiteiInfoConstants.FOLDER_PATH_SHITEI_INFO_JSON,
        "w",
        encoding="utf-8",
    ) as f:
        f.write(json_output)

    # print("指定表JSONファイルが生成されました。")
    logger.info("指定表JSONファイルが生成されました。")


def create_tokutei_info_json(**kwargs):
    # pandasを使用してExcelファイルを読み込む
    df = pd.read_excel(
        Constants.FOLDER_PATH_XML_TEMPLETE,
        sheet_name="XML構造設計書（様式第9）特定表",
        skiprows=8,
        nrows=2255,  # 第10行から第2255行まで読み込む
        usecols="A:Y",  # A列からY列まで読み込む
        engine=Constants.PackageName.PANDAS_ENGINE.value,
    )
    json_template = create_json_template(df, "Tokuteihyo")

    # JSONテンプレートを出力
    json_output = json.dumps(json_template, indent=4, ensure_ascii=False)

    # JSONファイルに出力
    with open(
        TokuteiInfoConstants.FOLDER_PATH_TOKUTEI_INFO_JSON,
        "w",
        encoding="utf-8",
    ) as f:
        f.write(json_output)

    # print("特定表JSONファイルが生成されました。")
    logger.info("特定表JSONファイルが生成されました。")


if __name__ == "__main__":
    create_shitei_info_json()
#    create_tokutei_info_json()
