def INSERT_ANCATE_INFO(insert_values):
    """
    関数名：調査表情報の登録
    """
    return f"""
        INSERT INTO ANCATE_INFO (
           ANCATE_ID,
           REPORT_NENDO,
           COMPANY_ID,
           COMPANY_NM,
           BUILDING_ID,
           BUILDING_NM,
           DEPT_NM,
           REP_NM,
           EXTENSION,
           INDUSTRIAL_CLASS_CD,
           POWER_AREA_CD,
           POWER_AREA_NM,
           POSTAL_CD,
           PREFECTURE,
           CITY,
           CHOME_BEYOND,
           COMPANY_OWNER_CD,
           COMPANY_OWNER_NM,
           POWER_DR_JOKO_CD,
           DR_DATE,
           GAS_COMPANY_ID,
           GAS_COMPANY_NM,
           HEAT_COMPANY_ID,
           HEAT_COMPANY_NM,
           LEASABLE_AREA_PG,
           LEASABLE_AREA_HD,
           LEASABLE_AREA_FP,
           LEASABLE_AREA_EP,
           LEASABLE_AREA_RP,
           ANBUN_RATE_PG,
           ANBUN_RATE_HD,
           ANBUN_RATE_FP,
           ANBUN_RATE_EP,
           ANBUN_RATE_RP,
           LAST_YEAR_CRUDE_OIL_EQUIVALENT,
           LAST_YEAR_WATER_AMOUNT,
           DENOMINATOR_TYPE,
           DENOMINATOR_VALUE,
           DAY_NIGHT_POWER_GRASP_FLAG,
           SUBSTATION_EXIST_FLG,
           SUBSTATION_ENERGY_GRASP_FLAG,
           SUBSTATION_WATER_GRASP_FLAG,
           SUBSTATION_FLOOR_AREA,
           BUILDING_FLOOR_AREA,
           SUBSTATION_FLOOR_RATE,
           POWER_GENERATION_AMOUNT,
           POWER_TRANSMISSION_AMOUNT,
           ANCATE_COMMENT,
           ENERGY_AMOUNT_DIFF_REASON,
           WATER_AMOUNT_DIFF_REASON,
           INFLOW_OUTFLOW_DIFF_REASON,
           ENERGY_AMOUNT_RATE,
           WATER_AMOUNT_RATE,
           ELECTRICITY_ENTERPRISE1_COMPANY_ID,
           ELECTRICITY_ENTERPRISE1_COMPANY_NM,
           ELECTRICITY_ENTERPRISE1_MENU_CD,
           ELECTRICITY_ENTERPRISE1_MENU_NM,
           ELECTRICITY_ENTERPRISE1_CO2_CD,
           NON_FOSSIL_RATIO1,
           ELECTRICITY_ENTERPRISE2_COMPANY_ID,
           ELECTRICITY_ENTERPRISE2_COMPANY_NM,
           ELECTRICITY_ENTERPRISE2_MENU_CD,
           ELECTRICITY_ENTERPRISE2_MENU_NM,
           ELECTRICITY_ENTERPRISE2_CO2_CD,
           NON_FOSSIL_RATIO2,
           DELETE_FLG,
           INSERT_NAME,
           INSERT_DATE,
           UPDATE_NAME,
           UPDATE_DATE
        ) VALUES {insert_values}
    """


def SELECT_ANCATE_INFO():
    """
    関数名：調査表情報の検索
    """
    return """
        SELECT
            ANCATE_ID,
            REPORT_NENDO,
            COMPANY_ID,
            COMPANY_NM,
            BUILDING_ID,
            BUILDING_NM,
            DEPT_NM,
            REP_NM,
            EXTENSION,
            INDUSTRIAL_CLASS_CD,
            POWER_AREA_CD,
            POWER_AREA_NM,
            POSTAL_CD,
            PREFECTURE,
            CITY,
            CHOME_BEYOND,
            COMPANY_OWNER_CD,
            COMPANY_OWNER_NM,
            POWER_DR_JOKO_CD,
            DR_DATE,
            GAS_COMPANY_ID,
            GAS_COMPANY_NM,
            HEAT_COMPANY_ID,
            HEAT_COMPANY_NM,
            LEASABLE_AREA_PG,
            LEASABLE_AREA_HD,
            LEASABLE_AREA_FP,
            LEASABLE_AREA_EP,
            LEASABLE_AREA_RP,
            ANBUN_RATE_PG,
            ANBUN_RATE_HD,
            ANBUN_RATE_FP,
            ANBUN_RATE_EP,
            ANBUN_RATE_RP,
            LAST_YEAR_CRUDE_OIL_EQUIVALENT,
            LAST_YEAR_WATER_AMOUNT,
            DENOMINATOR_TYPE,
            DENOMINATOR_VALUE,
            DAY_NIGHT_POWER_GRASP_FLAG,
            SUBSTATION_EXIST_FLG,
            SUBSTATION_ENERGY_GRASP_FLAG,
            SUBSTATION_WATER_GRASP_FLAG,
            SUBSTATION_FLOOR_AREA,
            BUILDING_FLOOR_AREA,
            SUBSTATION_FLOOR_RATE,
            POWER_GENERATION_AMOUNT,
            POWER_TRANSMISSION_AMOUNT,
            ANCATE_COMMENT,
            ENERGY_AMOUNT_DIFF_REASON,
            WATER_AMOUNT_DIFF_REASON,
            INFLOW_OUTFLOW_DIFF_REASON,
            ENERGY_AMOUNT_RATE,
            WATER_AMOUNT_RATE,
            ELECTRICITY_ENTERPRISE1_COMPANY_ID,
            ELECTRICITY_ENTERPRISE1_COMPANY_NM,
            ELECTRICITY_ENTERPRISE1_MENU_CD,
            ELECTRICITY_ENTERPRISE1_MENU_NM,
            ELECTRICITY_ENTERPRISE1_CO2_CD,
            NON_FOSSIL_RATIO1,
            ELECTRICITY_ENTERPRISE2_COMPANY_ID,
            ELECTRICITY_ENTERPRISE2_COMPANY_NM,
            ELECTRICITY_ENTERPRISE2_MENU_CD,
            ELECTRICITY_ENTERPRISE2_MENU_NM,
            ELECTRICITY_ENTERPRISE2_CO2_CD,
            NON_FOSSIL_RATIO2,
            DELETE_FLG,
            INSERT_NAME,
            INSERT_DATE,
            UPDATE_NAME,
            UPDATE_DATE
        FROM ANCATE_INFO
    """


def INSERT_OVERWRITE_ANCATE_INFO_BK():
    """
    関数名：調査表情報をバックアップ

    調査表情報のデータをバックアップする処理
    """
    return """
        INSERT OVERWRITE TABLE ANCATE_INFO_BK
        SELECT * FROM ANCATE_INFO
    """


def TRUNCATE_ANCATE_INFO():
    """
    関数名：調査表情報のデータをクリア

    調査表情報のデータをクリアする処理
    """
    return """
        TRUNCATE TABLE ANCATE_INFO
    """
