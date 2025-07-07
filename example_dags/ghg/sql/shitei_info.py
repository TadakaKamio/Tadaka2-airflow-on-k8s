def SELECT_SHITEI_INFO():
    """
    関数名：指定表情報の全件検索
    """
    return "SELECT * FROM SHITEI_INFO"


def INSERT_SHITEI_INFO(insert_values):
    """
    関数名：指定表情報の登録
    """
    return f"""
    INSERT INTO SHITEI_INFO (
        COMPANY_ID,
        BUILDING_ID,
        BUILDING_NAME,
        REPORT_NENDO,
        TABLE_0,
        TABLE_1,
        TABLE_2,
        TABLE_3,
        TABLE_4,
        TABLE_5,
        TABLE_6,
        TABLE_7,
        TABLE_8,
        TABLE_9,
        TABLE_10,
        DELETE_FLG,
        INSERT_NAME,
        INSERT_DATE,
        UPDATE_NAME,
        UPDATE_DATE
    ) VALUES {insert_values}
"""
