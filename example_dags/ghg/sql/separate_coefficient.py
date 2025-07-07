def INSERT_SEPARATE_COEFFICIENT(insert_values):
    """
    関数名：個別係数の登録
    """
    return f"""
       INSERT INTO SEPARATE_COEFFICIENT (
           ANCATE_ID,
           ENERGY_ID,
           ENERGY_NAME,
           NENDO,
           CONVERSION_COEFFICIENT,
           DELETE_FLG,
           INSERT_NAME,
           INSERT_DATE,
           UPDATE_NAME,
           UPDATE_DATE
        ) VALUES {insert_values}
    """


def INSERT_OVERWRITE_SEPARATE_COEFFICIENT_BK():
    """
    関数名：個別係数をバックアップ

    個別係数のデータをバックアップする処理
    """
    return """
        INSERT OVERWRITE TABLE SEPARATE_COEFFICIENT_BK
        SELECT * FROM SEPARATE_COEFFICIENT
    """
