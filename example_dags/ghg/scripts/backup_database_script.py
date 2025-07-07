from airflow.models import Variable
from ghg.common.hive_connector import HiveConnector
from ghg.common.log import MyAppLog, log_writer
from ghg.sql.ancate_info import INSERT_OVERWRITE_ANCATE_INFO_BK
from ghg.sql.energy_used_record_month_detail import (
    INSERT_OVERWRITE_ENERGY_USED_RECORD_MONTH_DETAIL_BK,
)
from ghg.sql.energy_used_record_year_detail import (
    INSERT_OVERWRITE_ENERGY_USED_RECORD_YEAR_DETAIL_BK,
)
from ghg.sql.separate_coefficient import INSERT_OVERWRITE_SEPARATE_COEFFICIENT_BK

logger = MyAppLog()

# Hive接続初期化
hive_connector = HiveConnector()


@log_writer(logger)
def backup_database(**kwargs):
    """
    関数名：対象テーブルをバックアップ

    対象テーブルをバックアップする処理

    パラメータ:
        なし

    戻り値:
        なし
    """
    try:
        logger.info("処理開始")

        # バックアップ対象テーブル名
        table_name = Variable.get("GHG_BACKUP_TABLE_NAME")
        logger.debug(table_name)

        # 各テーブル名に対応するバックアップ関数をマッピングする辞書
        backup_target_tables = {
            "ANCATE_INFO": execute_insert_overwrite_ancate_info_bk,
            "ENERGY_USED_RECORD_YEAR_DETAIL": execute_insert_overwrite_energy_used_record_year_detail_bk,
            "ENERGY_USED_RECORD_MONTH_DETAIL": execute_insert_overwrite_energy_used_record_month_detail_bk,
            "SEPARATE_COEFFICIENT": execute_insert_overwrite_separate_coefficient_bk,
        }

        if table_name == "ALL":
            # 全てのテーブルのバックアップ処理を実行
            for func_name, func in backup_target_tables.items():
                logger.info(f"バックアップ開始：{func_name}")
                func()  # 関数を実行
                logger.info(f"バックアップ終了：{func_name}")
        else:
            if table_name in backup_target_tables:
                logger.info(f"バックアップ開始：{table_name}")
                backup_target_tables[table_name]()
                logger.info(f"バックアップ終了：{table_name}")
            else:
                logger.error(
                    f"'{table_name}'はバックアップ対象テーブルではないです。処理終了。"
                )

    except Exception as e:
        logger.error(f"エラーが発生しました: {e}")
        raise e
    finally:
        # 接続を閉じる
        hive_connector.close_connection()
        logger.info("処理終了")


@log_writer(logger)
def execute_insert_overwrite_ancate_info_bk():
    """
    関数名：調査表情報をバックアップ

    調査表情報のデータをバックアップする処理

    パラメータ:
        なし

    戻り値:
        なし
    """
    insert_sql = INSERT_OVERWRITE_ANCATE_INFO_BK()
    logger.debug(insert_sql)
    hive_connector.execute_query(insert_sql)


@log_writer(logger)
def execute_insert_overwrite_energy_used_record_year_detail_bk():
    """
    関数名：エネルギー使用実績明細(年別)をバックアップ

    エネルギー使用実績明細(年別)のデータをバックアップする処理

    パラメータ:
        なし

    戻り値:
        なし
    """
    insert_sql = INSERT_OVERWRITE_ENERGY_USED_RECORD_YEAR_DETAIL_BK()
    logger.debug(insert_sql)
    hive_connector.execute_query(insert_sql)


@log_writer(logger)
def execute_insert_overwrite_energy_used_record_month_detail_bk():
    """
    関数名：エネルギー使用実績明細(月別)をバックアップ

    エネルギー使用実績明細(月別)のデータをバックアップする処理

    パラメータ:
        なし

    戻り値:
        なし
    """
    insert_sql = INSERT_OVERWRITE_ENERGY_USED_RECORD_MONTH_DETAIL_BK()
    logger.debug(insert_sql)
    hive_connector.execute_query(insert_sql)


@log_writer(logger)
def execute_insert_overwrite_separate_coefficient_bk():
    """
    関数名：個別係数をバックアップ

    個別係数のデータをバックアップする処理

    パラメータ:
        なし

    戻り値:
        なし
    """
    insert_sql = INSERT_OVERWRITE_SEPARATE_COEFFICIENT_BK()
    logger.debug(insert_sql)
    hive_connector.execute_query(insert_sql)


if __name__ == "__main__":
    backup_database()
