def SELECT_NON_FOSSIL_RATIO_INFO_MST():
    """
    関数名：非化石割合情報マスタの検索
    """
    return """
        SELECT
            ELECTRICITY_ENTERPRISE_COMPANY_NM,
            ELECTRICITY_ENTERPRISE_MENU_NM,
            NON_FOSSIL_RATIO,
            DELETE_FLG,
            INSERT_NAME,
            INSERT_DATE,
            UPDATE_NAME,
            UPDATE_DATE
        FROM NON_FOSSIL_RATIO_INFO_MST
    """
