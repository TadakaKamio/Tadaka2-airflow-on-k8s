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

# from ghg.scripts.edit_output_data_script import check_tokutei_info_json
from ghg.sql.company_mst import SELECT_COMPANY_MST_BY_ID
from ghg.sql.tokutei_info import SELECT_TOKUTEI_INFO

logger = MyAppLog()

# Hive接続初期化
hive_connector = HiveConnector()


@log_writer(logger)
def export_tokutei_xml(**kwargs):
    """
    関数名：特定表のXMLを出力

    特定表のXMLを出力する処理

    パラメータ:
        なし

    戻り値:
        なし
    """

    try:
        logger.info("処理開始")

        # 特定表情報の全件検索
        results = execute_select_tokutei_info()

        # dicttoxmlをインストール
        check_install_package(Constants.PackageName.DICTTOXML.value)

        if not results:
            msg = "特定表情報(TOKUTEI_INFO)にデータが存在しない。"
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
def execute_select_tokutei_info():
    """
    関数名：特定表情報の全件検索

    特定表情報の全件検索する処理

    パラメータ:
        なし

    戻り値:
        なし
    """
    # 特定表情報の全件検索
    select_sql = SELECT_TOKUTEI_INFO()

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
    # 報告年度 = 報告対象年度 + 1
    houkoku_nendo = result[1] + 1
    # 「特定－表紙」
    table_0_json = json.loads(cleaned_json(result[2]))
    # 「特定－第1表」
    table_1_json = json.loads(cleaned_json(result[3]))
    # 「特定－第2表」
    table_2_json = json.loads(cleaned_json(result[4]))
    # 「特定－第3表」
    table_3_json = json.loads(cleaned_json(result[5]))
    # 「特定－第4表」
    table_4_json = json.loads(cleaned_json(result[6]))
    # 「特定－第5表」
    table_5_json = json.loads(cleaned_json(result[7]))
    # 「特定－第6表」
    table_6_json = json.loads(cleaned_json(result[8]))
    # 「特定－第7表」
    table_7_json = json.loads(cleaned_json(result[9]))
    # 「特定－第8表」
    table_8_json = json.loads(cleaned_json(result[10]))
    # 「特定－第9表」
    table_9_json = json.loads(cleaned_json(result[11]))
    # 「特定－第10表」
    table_10_json = json.loads(cleaned_json(result[12]))
    # 「特定－第11表」
    table_11_json = json.loads(cleaned_json(result[13]))
    # 「特定－第12表」
    table_12_json = json.loads(cleaned_json(result[14]))

    json_template = {
        "Tokuteihyo": {
            "Houkoku_Nendo": houkoku_nendo,  # 報告年度
            "Tokutei_00": table_0_json,  # 表紙
            "Tokutei_01": table_1_json,  # 特定－第1表
            "Tokutei_02": table_2_json,  # 特定－第2表
            "Tokutei_03": table_3_json,  # 特定－第3表
            "Tokutei_04": table_4_json,  # 特定－第4表
            "Tokutei_05": table_5_json,  # 特定－第5表
            "Tokutei_06": table_6_json,  # 特定－第6表
            "Tokutei_07": table_7_json,  # 特定－第7表
            "Tokutei_08": table_8_json,  # 特定－第8表
            "Tokutei_09": table_9_json,  # 特定－第9表
            "Tokutei_10": table_10_json,  # 特定－第10表
            "Tokutei_11": table_11_json,  # 特定－第11表
            "Tokutei_12": table_12_json,  # 特定－第12表
            "Ninteitoukatsu": {  # 認定総括表
                "Jigyosha_No": "",  # 認定統括事業者番号
                "Jigyosha_Name": "",  # 事業者名称
                "Hojin_Name": "",  # 法人名
                "Hojin_Name_En": "",  # 法人名（英語表記）
                "Hojin_No": "",  # 法人番号
                "MeigaraCd": "",  # 銘柄コード
                "Kanrikankei_Array": [  # 管理関係事業者_Array
                    {
                        "Kanrikankei": {  # 管理関係事業者
                            "Jigyosha_No": "",  # 管理関係事業者番号
                            "Jigyosha_Name": "",  # 事業者名称
                            "Hojin_Name": "",  # 法人名
                            "Hojin_Name_En": "",  # 法人名（英語表記）
                            "Hojin_No": "",  # 法人番号
                            "MeigaraCd": "",  # 銘柄コード
                        }
                    }
                ],
            },
        }
    }

    # 会社マスタを検索
    company_um = execute_select_company_mst(company_id)

    # logger.info(f"会社略称は:{company_um}のデータチェックを処理開始")
    # error_occurred = check_tokutei_info_json(json_template)
    # if error_occurred is True:
    #     return
    # logger.info(f"会社略称は:{company_um}のデータチェックを処理結束")

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
    sub_path = Variable.get("GHG_HADOOP_OUTPUTFILES_TOKUTEI_INFO_XML_PATH")

    # Hadoop対象フォルダを取得
    target_path = get_joined_path(base_path, sub_path, company_um)
    logger.debug(f"target_path {target_path}")

    # ファイル名：会社名略称_システム日時(東京のタイムスタンプ).xml
    file_name = f"{company_id}_{current_timestamp}{Constants.XMLExtension.XML.value}"
    file_path = f"{target_path}/{file_name}"

    # Hadoopを使ってファイルに書き込む
    put_file_to_hadoop(pretty_xml, file_path)
    logger.info(f"XMLファイル「{file_path}」が生成されました。")


if __name__ == "__main__":
    export_tokutei_xml()
