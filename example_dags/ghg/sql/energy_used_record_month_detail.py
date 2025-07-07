def INSERT_ENERGY_USED_RECORD_MONTH_DETAIL(insert_values):
    """
    関数名：エネルギー使用実績明細(月別)の登録
    """
    return f"""
        INSERT INTO ENERGY_USED_RECORD_MONTH_DETAIL (
            ANCATE_ID,
            BUILDING_NM,
            ENERGY_ID,
            ENERGY_NAME,
            REPORT_NENDO,
            TARGET_MONTH,
            INPUT_UNIT,
            ENERGY_USAGE_AMOUNT,
            DELETE_FLG,
            INSERT_NAME,
            INSERT_DATE,
            UPDATE_NAME,
            UPDATE_DATE
        ) VALUES {insert_values}
    """


def INSERT_OVERWRITE_ENERGY_USED_RECORD_MONTH_DETAIL_BK():
    """
    関数名：エネルギー使用実績明細(月別)をバックアップ

    エネルギー使用実績明細(月別)のデータをバックアップする処理
    """
    return """
        INSERT OVERWRITE TABLE ENERGY_USED_RECORD_MONTH_DETAIL_BK
        SELECT * FROM ENERGY_USED_RECORD_MONTH_DETAIL
    """
