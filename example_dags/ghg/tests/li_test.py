import json
import sqlite3

import pandas as pd
from ghg.common.hive_connector import HiveConnector
from ghg.common.log import MyAppLog, log_writer
from ghg.common.settings_tokutei_info import (
    ELECTRICITY_LEVELING_TIME_FACTOR,
    NON_FOSSIL_FUEL_COMPENSATION_FACTOR,
    OIL_CONV_FACTOR,
)
from ghg.common.utils import mul, turn_excel_item_to_dict

logger = MyAppLog()
# Hive接続初期化
hive_connector = HiveConnector()


def test(**kwargs):
    tables = get_all_table_data()
    get_table3_data(tables, "HD")


def get_dataframe(cursor, table_name, where_option=""):
    from impala.util import as_pandas

    query = f"select * from {table_name}"
    if where_option:
        query += f" where {where_option}"
    cursor.execute(query)
    return as_pandas(cursor)


def get_all_table_data():
    # DBから関連のテーブルを取得
    if __name__ == "__main__":
        year_energy = test_query("select * from energy_used_record_year_detail")
        kubun_mst = test_query("select * from kubun_mst")
        month_energy = test_query("select * from energy_used_record_month_detail")
        ancate_info = test_query("select * from ancate_info")
        optimal_factor = test_query(
            "select * from require_optimization_coefficient_for_month_mst"
        )
        energy_mst = test_query("select * from energy_mst where nendo = 2023")

        year_energy.columns = year_energy.columns.str.lower()
        kubun_mst.columns = kubun_mst.columns.str.lower()
        month_energy.columns = month_energy.columns.str.lower()
        ancate_info.columns = ancate_info.columns.str.lower()
        optimal_factor.columns = optimal_factor.columns.str.lower()
        energy_mst.columns = energy_mst.columns.str.lower()
    else:
        conn = hive_connector.hive_connect()
        cursor = conn.cursor()

        year_energy = get_dataframe(cursor, "energy_used_record_year_detail")
        kubun_mst = get_dataframe(cursor, "kubun_mst")
        month_energy = get_dataframe(cursor, "energy_used_record_month_detail")
        ancate_info = get_dataframe(cursor, "ancate_info")
        optimal_factor = get_dataframe(
            cursor, "require_optimization_coefficient_for_month_mst"
        )
        energy_mst = get_dataframe(cursor, "energy_mst", "nendo = 2023")

        cursor.close()
        conn.close()

        # SQL文に「*」を使って取得したの列名は所属テーブル名を付けっていますので、
        # 下記の処理で、テーブル名を取り除く
        for df in [
            year_energy,
            kubun_mst,
            month_energy,
            ancate_info,
            optimal_factor,
            energy_mst,
        ]:
            df.columns = df.columns.str.split(".").str[-1]

    tables = {}
    tables["year_energy"] = year_energy
    tables["kubun_mst"] = kubun_mst
    tables["month_energy"] = month_energy
    tables["ancate_info"] = ancate_info
    tables["optimal_factor"] = optimal_factor
    tables["energy_mst"] = energy_mst

    return tables


@log_writer(logger)
def get_table3_data(tables, company_um):
    # tablesから今回使用のデータを取得する
    year_energy = tables["year_energy"][
        [
            "ancate_id",
            "energy_id",
            "energy_amount",
            "new_energy_coefficient",
            "old_energy_coefficient",
            "sale_secondary_energy_amount",
            "unused_heat_amount",
        ]
    ]
    kubun_mst = tables["kubun_mst"][["bunrui_cd", "kbn_cd", "kbn_name"]]
    kubun_0015 = kubun_mst[kubun_mst["bunrui_cd"] == "0015"]
    kubun_0002 = kubun_mst[kubun_mst["bunrui_cd"] == "0002"]
    # 原単位分母の名称と単位を追加する
    kubun_0002["denominator_nm"] = kubun_0002["kbn_name"].str.extract(r"(^[^\[]+)")
    kubun_0002["denominator_tani"] = kubun_0002["kbn_name"].str.extract(r"\[(.*?)\]")
    ancate_info = tables["ancate_info"][
        [
            "ancate_id",
            "report_nendo",
            "substation_energy_grasp_flag",
            "substation_floor_rate",
            "power_area_cd",
        ]
    ]
    ancate_info2 = tables["ancate_info"][
        [
            "ancate_id",
            "report_nendo",
            "denominator_type",
            "denominator_value",
            "industrial_class_cd",
            "anbun_rate_hd",
            "anbun_rate_pg",
            "anbun_rate_ep",
            "anbun_rate_rp",
        ]
    ]
    if company_um == "HD":
        ancate_info2["anbun_rate"] = ancate_info2["anbun_rate_hd"]
    elif company_um == "PG":
        ancate_info2["anbun_rate"] = ancate_info2["anbun_rate_pg"]
    elif company_um == "EP":
        ancate_info2["anbun_rate"] = ancate_info2["anbun_rate_ep"]
    elif company_um == "RP":
        ancate_info2["anbun_rate"] = ancate_info2["anbun_rate_rp"]
    else:
        ancate_info2["anbun_rate"] = 0
    ancate_info2 = ancate_info2[ancate_info2["anbun_rate"] > 0]

    month_energy = tables["month_energy"][
        ["energy_id", "energy_usage_amount", "ancate_id", "target_month"]
    ]
    month_energy_power = month_energy[
        month_energy["energy_id"].isin(["D01", "D03", "D04", "D06", "D07", "D08"])
    ]
    optimal_factor = tables["optimal_factor"][
        [
            "target_month",
            "power_area_cd",
            "report_nendo",
            "require_optimization_coefficient",
        ]
    ]
    energy_mst = tables["energy_mst"]

    # 合理化データを作成
    df1 = year_energy.merge(
        kubun_0015, how="left", left_on="energy_id", right_on="kbn_cd"
    )
    df1 = df1.where(df1.notnull(), None)

    # 検索項目を処理する
    df1["data_flg"] = 0
    df1["energy_amount_gj"] = df1.apply(
        lambda row: (
            0
            if row["energy_id"] in ["D02", "D05"]
            else mul(row["energy_amount"], row["new_energy_coefficient"])
        ),
        axis=1,
    )
    df1["energy_amount_gj_2023"] = df1.apply(
        lambda row: (
            mul(row["energy_amount"], row["old_energy_coefficient"])
            if row["energy_id"] in ["D02", "D05"]
            else mul(row["energy_amount"], row["old_energy_coefficient"])
        ),
        axis=1,
    )
    df1["sale_secondary_energy_amount_gj"] = df1.apply(
        lambda row: (
            0
            if row["energy_id"] in ["D02", "D05"]
            else mul(row["sale_secondary_energy_amount"], row["new_energy_coefficient"])
        ),
        axis=1,
    )
    df1["sale_secondary_energy_amount_gj_2023"] = df1.apply(
        lambda row: (
            0
            if row["energy_id"] in ["D02", "D05"]
            else mul(row["sale_secondary_energy_amount"], row["old_energy_coefficient"])
        ),
        axis=1,
    )
    df1["unused_heat_amount_gj"] = df1.apply(
        lambda row: (
            0
            if row["energy_id"] in ["D02", "D05"]
            else mul(row["unused_heat_amount"], row["new_energy_coefficient"])
        ),
        axis=1,
    )
    df1["unused_heat_amount_gj_2023"] = df1.apply(
        lambda row: (
            0
            if row["energy_id"] in ["D02", "D05"]
            else mul(row["unused_heat_amount"], row["old_energy_coefficient"])
        ),
        axis=1,
    )

    # 検索条件
    df1 = df1[(df1["kbn_cd"].notnull()) | df1["energy_id"].isin(["D02", "D05"])]

    # 最適化電気データを作成
    df2 = month_energy_power.merge(ancate_info, on=["ancate_id"]).merge(
        optimal_factor, on=["target_month", "power_area_cd", "report_nendo"]
    )

    # 集計処理
    # 変電所以外の按分比率
    df2["use_rate"] = df2.apply(
        lambda row: (
            row["substation_floor_rate"]
            if row["substation_energy_grasp_flag"] == "1"
            else 1
        ),
        axis=1,
    )
    # 最適化電気の使用量GJ
    df2["energy_gj"] = (
        df2["energy_usage_amount"]
        * df2["require_optimization_coefficient"]
        * df2["use_rate"]
    )
    df2 = (
        df2.groupby(["ancate_id", "energy_id"])
        .agg(energy_amount_gj=("energy_gj", "sum"))
        .reset_index()
    )
    # 検索項目を処理する
    df2["data_flg"] = 1
    df2["energy_amount_gj_2023"] = 0
    df2["sale_secondary_energy_amount_gj"] = 0
    df2["sale_secondary_energy_amount_gj_2023"] = 0
    df2["unused_heat_amount_gj"] = 0
    df2["unused_heat_amount_gj_2023"] = 0

    df_union = pd.concat([df1, df2])
    df_merge = (
        df_union.merge(ancate_info2, on="ancate_id")
        .merge(
            energy_mst,
            left_on=["energy_id", "report_nendo"],
            right_on=["energy_id", "nendo"],
        )
        .merge(kubun_0002, left_on=["denominator_type"], right_on=["kbn_cd"])
    )

    # 集計時使用の関数
    def genyu_sum(series, condition, rate):
        return (series[condition] * rate).sum() * OIL_CONV_FACTOR

    df = df_merge
    result = (
        df.groupby(["industrial_class_cd", "denominator_type"])
        .agg(
            denominator_nm=("denominator_nm", "max"),
            denominator_tani=("denominator_tani", "max"),
            denominator_value=("denominator_value", "sum"),
            a=(
                "energy_amount_gj",
                lambda x: round(
                    genyu_sum(
                        x,
                        (df["data_flg"] != 1) & (~df["energy_id"].isin(["D02", "D05"])),
                        df["anbun_rate"],
                    )
                ),
            ),
            a_2023=(
                "energy_amount_gj_2023",
                lambda x: round(
                    genyu_sum(
                        x,
                        (df["data_flg"] != 1) & (~df["energy_id"].isin(["D02", "D05"])),
                        df["anbun_rate"],
                    )
                ),
            ),
            a2=(
                "energy_amount_gj",
                lambda x: round(
                    genyu_sum(
                        x,
                        (df["data_flg"] != 1)
                        & (~df["energy_id"].isin(["D02", "D05"]))
                        & (df["energy_type_cd"] == "B"),
                        df["anbun_rate"] * NON_FOSSIL_FUEL_COMPENSATION_FACTOR,
                    )
                    + genyu_sum(
                        x,
                        (df["data_flg"] != 1)
                        & (~df["energy_id"].isin(["D02", "D05"]))
                        & (df["energy_type_cd"] != "B"),
                        df["anbun_rate"],
                    )
                ),
            ),
            a2_2023=(
                "energy_amount_gj_2023",
                lambda x: round(
                    genyu_sum(
                        x,
                        (df["data_flg"] != 1) & (~df["energy_id"].isin(["D02", "D05"])),
                        df["anbun_rate"],
                    )
                ),
            ),
            b=(
                "sale_secondary_energy_amount_gj",
                lambda x: round(
                    genyu_sum(
                        x,
                        (df["data_flg"] != 1) & (~df["energy_id"].isin(["D02", "D05"])),
                        df["anbun_rate"],
                    )
                ),
            ),
            b_2023=(
                "sale_secondary_energy_amount_gj_2023",
                lambda x: round(
                    genyu_sum(
                        x,
                        (df["data_flg"] != 1) & (~df["energy_id"].isin(["D02", "D05"])),
                        df["anbun_rate"],
                    )
                ),
            ),
            b2=(
                "unused_heat_amount_gj",
                lambda x: round(
                    genyu_sum(
                        x,
                        (df["energy_type_cd"] == "C")
                        & (df["data_flg"] != 1)
                        & (~df["energy_id"].isin(["D02", "D05"])),
                        df["anbun_rate"],
                    )
                ),
            ),
            b2_2023=(
                "unused_heat_amount_gj_2023",
                lambda x: round(
                    genyu_sum(
                        x,
                        (df["energy_type_cd"] == "C")
                        & (df["data_flg"] != 1)
                        & (~df["energy_id"].isin(["D02", "D05"])),
                        df["anbun_rate"],
                    )
                ),
            ),
            heijyunka_a2=(
                "energy_amount_gj",
                lambda x: round(
                    genyu_sum(
                        x,
                        ~(
                            ((df["data_flg"] == 0))
                            & (
                                df["energy_id"].isin(
                                    ["D01", "D03", "D04", "D06", "D07", "D08"]
                                )
                            )
                        )
                        & (~df["energy_id"].isin(["D02", "D05"]))
                        & (df["energy_type_cd"] == "B"),
                        df["anbun_rate"] * NON_FOSSIL_FUEL_COMPENSATION_FACTOR,
                    )
                    + genyu_sum(
                        x,
                        ~(
                            ((df["data_flg"] == 0))
                            & (
                                df["energy_id"].isin(
                                    ["D01", "D03", "D04", "D06", "D07", "D08"]
                                )
                            )
                        )
                        & (~df["energy_id"].isin(["D02", "D05"]))
                        & (df["energy_type_cd"] != "B"),
                        df["anbun_rate"],
                    )
                ),
            ),
            heijyunka_a2_2023=(
                "energy_amount_gj_2023",
                lambda x: round(
                    genyu_sum(
                        x,
                        (df["data_flg"] != 1) & (df["energy_id"].isin(["D02", "D05"])),
                        df["anbun_rate"] * ELECTRICITY_LEVELING_TIME_FACTOR,
                    )
                    + genyu_sum(
                        x,
                        (df["data_flg"] != 1) & (~df["energy_id"].isin(["D02", "D05"])),
                        df["anbun_rate"],
                    )
                ),
            ),
        )
        .reset_index()
    )

    logger.debug(result)

    # turn DataFrame data to table
    table_data = list(result.to_records(index=False))

    return table_data


def get_json(file_path, sheet_name, usecols, lastcol):
    excel_data = pd.read_excel(
        file_path,
        sheet_name=sheet_name,
        header=1,
        usecols=usecols,
        engine="openpyxl",
    )

    # NaN値をNoneに変換
    pandas_df = excel_data.map(lambda x: None if pd.isna(x) else x)

    dict_data, _ = turn_excel_item_to_dict(pandas_df, 0, 1, 0, lastcol)

    jsonData = json.dumps(dict_data, ensure_ascii=False)

    return jsonData


def test_query(query):
    from impala.util import as_pandas

    local_db_path = r"C:\ws\db_ghg.db"
    with sqlite3.connect(local_db_path) as conn:
        try:
            cursor = conn.cursor()
            cursor.execute(query)
            return as_pandas(cursor)
        finally:
            cursor.close()


if __name__ == "__main__":
    test()
