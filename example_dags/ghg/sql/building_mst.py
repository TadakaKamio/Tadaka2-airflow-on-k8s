def SELECT_BUILDING_MST_BY_NAME(select_keyword):
    """
    関数名：建物IDの検索
    """
    return f"""
        SELECT BUILDING_ID FROM BUILDING_MST WHERE BUILDING_NM = '{select_keyword}'
    """
