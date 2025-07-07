import json
import logging
from xml.dom.minidom import parseString

import ghg.common.settings as Constants
from airflow.models import Variable
from ghg.common.hive_connector import HiveConnector
from ghg.common.log import MyAppLog, log_writer
from ghg.common.utils import (
    check_install_package,
    cleaned_json,
    get_current_tokyo_timestamp,
    get_joined_path,
    put_file_to_hadoop,
)

# from ghg.scripts.edit_output_data_script import check_shitei_info_json
from ghg.sql.company_mst import SELECT_COMPANY_MST_BY_ID
from ghg.sql.shitei_info import SELECT_SHITEI_INFO

logger = MyAppLog()

# Hive接続初期化
hive_connector = HiveConnector()


@log_writer(logger)
def export_shitei_xml(**kwargs):
    """
    関数名：指定表のXMLを出力

    指定表のXMLを出力する処理

    パラメータ:
        なし

    戻り値:
        なし
    """

    try:
        logger.info("処理開始")

        # 指定表情報の全件検索
        results = execute_select_shitei_info()
        # dicttoxmlをインストール
        check_install_package(Constants.PackageName.DICTTOXML.value)

        if not results:
            msg = "指定表情報(SHITEI_INFO)にデータが存在しない。"
            logger.error(msg)
            raise Exception(msg)

        for result in results:
            # XML出力
            export_xml(result)

    except Exception as e:
        logger.error(f"エラーが発生しました: {e}")
        raise e
    finally:
        # 接続を閉じる
        hive_connector.close_connection()
        logger.info("処理終了")


@log_writer(logger)
def execute_select_shitei_info():
    """
    関数名：指定表情報の全件検索

    指定表情報の全件検索する処理

    パラメータ:
        なし

    戻り値:
        なし
    """
    # 指定表情報の全件検索
    select_sql = SELECT_SHITEI_INFO()

    results = hive_connector.execute_query(select_sql, Constants.DBoperation.FETCHALL)

    return results


@log_writer(logger)
def execute_select_company_mst(company_id):
    """
    関数名：会社マスタの検索

    会社マスタの検索処理

    パラメータ:
        params: 会社ID

    戻り値:
        会社名略称
    """
    # 会社IDを取得
    select_sql = SELECT_COMPANY_MST_BY_ID(company_id)
    logger.debug(select_sql)

    results = hive_connector.execute_query(select_sql, Constants.DBoperation.FETCHONE)
    companyUm = results[0]
    logger.debug(companyUm)

    return companyUm


@log_writer(logger)
def export_xml(result):

    import dicttoxml

    # 会社ID
    company_id = result[0]
    # 建物ID
    building_id = result[1]
    # 報告年度
    houkoku_nendo = result[3]
    # 「指定－第0表」
    table_0_json = json.loads(cleaned_json(result[4]))
    # 「指定－第1表」
    table_1_json = json.loads(cleaned_json(result[5]))
    # 「指定－第2表」
    table_2_json = json.loads(cleaned_json(result[6]))
    # 「指定－第3表」
    table_3_json = json.loads(cleaned_json(result[7]))
    # 「指定－第4表」
    table_4_json = json.loads(cleaned_json(result[8]))
    # 「指定－第5表」
    table_5_json = json.loads(cleaned_json(result[9]))
    # 「指定－第6表」
    table_6_json = json.loads(cleaned_json(result[10]))
    # 「指定－第7表」
    table_7_json = json.loads(cleaned_json(result[11]))
    # 「指定－第8表」
    table_8_json = json.loads(cleaned_json(result[12]))
    # 「指定－第9表」
    table_9_json = json.loads(cleaned_json(result[13]))
    # 「指定－第10表」
    table_10_json = json.loads(cleaned_json(result[14]))

    json_template = {
        "Shiteihyo": {
            "Houkoku_Nendo": houkoku_nendo,  # 報告年度
            "Tokutei": table_0_json,  # 事業者情報
            "Shitei": {
                "Shitei_01": table_1_json,  # 指定－第1表
                "Shitei_02": table_2_json,  # 指定－第2表
                "Shitei_03": table_3_json,  # 指定－第3表
                "Shitei_04": table_4_json,  # 指定－第4表
                "Shitei_05": table_5_json,  # 指定－第5表
                "Shitei_06": table_6_json,  # 指定－第6表
                "Shitei_07": table_7_json,  # 指定－第7表
                "Shitei_08": table_8_json,  # 指定－第8表
                "Shitei_09": table_9_json,  # 指定－第9表
                "Shitei_10": table_10_json,  # 指定－第10表
            },
        }
    }

    # 会社マスタを検索
    company_um = execute_select_company_mst(company_id)

    # logger.info(
    #     f"会社略称は:{company_um}、建物IDは{building_id}のデータチェックを処理開始"
    # )
    # error_occurred = check_shitei_info_json(json_template)
    # if error_occurred is True:
    #     return
    # logger.info(
    #     f"会社略称は:{company_um}、建物IDは{building_id}のデータチェックを処理結束"
    # )

    logger.info("XMLファイルが生成処理を開始")
    # XMLデータを生成
    loggers = logging.getLogger("dicttoxml")
    loggers.setLevel(logging.ERROR)
    xml_data = (
        dicttoxml.dicttoxml(
            json_template, attr_type=False, root=False, return_bytes=False
        )
        .replace("<item>", "")
        .replace("</item>", "")
    )

    dom = parseString(xml_data)

    root = dom.documentElement
    root.setAttribute("xmlns:xsd", "http://www.w3.org/2001/XMLSchema")
    root.setAttribute("xmlns:xsi", "http://www.w3.org/2001/XMLSchema-instance")

    pretty_xml = dom.toprettyxml(indent="    ")

    pretty_xml = pretty_xml.replace(
        '<?xml version="1.0" ?>', '<?xml version="1.0" encoding="utf-8"?>'
    )

    # 現在日時
    current_timestamp = get_current_tokyo_timestamp()

    # Hadoop対象フォルダを指定
    base_path = Variable.get("GHG_HADOOP_BASE_PATH")
    sub_path = Variable.get("GHG_HADOOP_OUTPUTFILES_SHITEI_INFO_XML_PATH")

    # Hadoop対象フォルダを取得
    target_path = get_joined_path(base_path, sub_path, company_um)
    logger.debug(f"target_path {target_path}")

    # ファイル名：会社名略称_建物ID_システム日時(東京のタイムスタンプ).xml
    file_name = (
        f"{company_um}_{building_id}_{current_timestamp}"
        f"{Constants.XMLExtension.XML.value}"
    )
    file_path = f"{target_path}/{file_name}"

    # Hadoopを使ってファイルに書き込む
    put_file_to_hadoop(pretty_xml, file_path)
    logger.info(f"XMLファイル「{file_path}」が生成されました。")


if __name__ == "__main__":
    export_shitei_xml()
