def INSERT_ENERGY_USED_RECORD_YEAR_DETAIL(insert_values):
    """
    関数名：エネルギー使用実績明細(年別)の登録
    """
    return f"""
        INSERT INTO ENERGY_USED_RECORD_YEAR_DETAIL (
           ANCATE_ID,
           BUILDING_NM,
           ENERGY_ID,
           ENERGY_NAME,
           REPORT_NENDO,
           OLD_ENERGY_COEFFICIENT,
           NEW_ENERGY_COEFFICIENT,
           REPORT_UNIT,
           ENERGY_AMOUNT,
           SALE_SECONDARY_ENERGY_AMOUNT,
           EXTERNAL_SUPPLY_FUEL_AMOUNT,
           UNUSED_HEAT_AMOUNT,
           DELETE_FLG,
           INSERT_NAME,
           INSERT_DATE,
           UPDATE_NAME,
           UPDATE_DATE
        ) VALUES {insert_values}
    """


def INSERT_OVERWRITE_ENERGY_USED_RECORD_YEAR_DETAIL_BK():
    """
    関数名：エネルギー使用実績明細(年別)をバックアップ

    エネルギー使用実績明細(年別)のデータをバックアップする処理
    """
    return """
        INSERT OVERWRITE TABLE ENERGY_USED_RECORD_YEAR_DETAIL_BK
        SELECT * FROM ENERGY_USED_RECORD_YEAR_DETAIL
    """
