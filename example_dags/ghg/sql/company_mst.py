def SELECT_COMPANY_MST_BY_NAME(select_keyword):
    """
    関数名：会社IDの検索
    """
    return f"""
        SELECT COMPANY_ID FROM COMPANY_MST WHERE COMPANY_UM = '{select_keyword}'
    """


def SELECT_COMPANY_MST_BY_ID(select_keyword):
    """
    関数名：会社略称の検索
    """
    return f"""
        SELECT COMPANY_UM FROM COMPANY_MST WHERE COMPANY_ID = '{select_keyword}'
    """
