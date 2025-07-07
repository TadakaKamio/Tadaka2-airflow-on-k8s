from collections import namedtuple


# 特定表情報の全件検索
def SELECT_TOKUTEI_INFO():
    return "SELECT * FROM TOKUTEI_INFO"


# 特定表情報の登録
def INSERT_TOKUTEI_INFO(insert_values):
    return f"""
        INSERT INTO TOKUTEI_INFO (
            COMPANY_ID,
            REPORT_NENDO,
            TOKUTEI_00,
            TOKUTEI_01,
            TOKUTEI_02,
            TOKUTEI_03,
            TOKUTEI_04,
            TOKUTEI_05,
            TOKUTEI_06,
            TOKUTEI_07,
            TOKUTEI_08,
            TOKUTEI_09,
            TOKUTEI_10,
            TOKUTEI_11,
            TOKUTEI_12,
            DELETE_FLG,
            INSERT_NAME,
            INSERT_DATE,
            UPDATE_NAME,
            UPDATE_DATE
        ) VALUES {insert_values}
    """


def SELECT_DENKI(companyUM, reportNendo):
    """
    指定会社、報告年度の電気のデータを取得するSQL文
    パラメータ：
        company：会社名略称
        reportNendo：報告年度
    戻り値：
        SQL文
    """
    return f"""
        -- 電気事業者①の情報を取得
        SELECT
            ai1.ELECTRICITY_ENTERPRISE1_COMPANY_NM AS COMPANY_NM,
            ai1.ELECTRICITY_ENTERPRISE1_MENU_NM AS MENU_NM,
            ai1.NON_FOSSIL_RATIO1 AS RATIO,
            ai1.BUILDING_NM,
            ai1.INDUSTRIAL_CLASS_CD,
            eu11.ENERGY_AMOUNT * ai1.ANBUN_RATE_{companyUM} AS ENERGY_AMOUNT_DAY,
            eu12.ENERGY_AMOUNT * ai1.ANBUN_RATE_{companyUM} AS ENERGY_AMOUNT_NIGHT
        FROM
            ANCATE_INFO ai1
            -- 昼間買電量を取得する
            LEFT JOIN ENERGY_USED_RECORD_YEAR_DETAIL eu11 ON (
                eu11.ANCATE_ID = ai1.ANCATE_ID
                AND eu11.ENERGY_ID = 'D01'
            )
            -- 夜間買電量を取得する
            LEFT JOIN ENERGY_USED_RECORD_YEAR_DETAIL eu12 ON (
                eu12.ANCATE_ID = ai1.ANCATE_ID
                AND eu12.ENERGY_ID = 'D03'
            )
        WHERE
            ai1.ANBUN_RATE_{companyUM} > 0
            AND ai1.REPORT_NENDO = {reportNendo}
            AND (
                eu11.ENERGY_AMOUNT > 0
                OR eu12.ENERGY_AMOUNT > 0
            )
        UNION ALL
        -- 電気事業者②の情報を取得
        SELECT
            ai2.ELECTRICITY_ENTERPRISE2_COMPANY_NM AS COMPANY_NM,
            ai2.ELECTRICITY_ENTERPRISE2_MENU_NM AS MENU_NM,
            ai2.NON_FOSSIL_RATIO2 AS RATIO,
            ai2.BUILDING_NM,
            ai2.INDUSTRIAL_CLASS_CD,
            eu21.ENERGY_AMOUNT * ai2.ANBUN_RATE_{companyUM} AS ENERGY_AMOUNT_DAY,
            eu22.ENERGY_AMOUNT * ai2.ANBUN_RATE_{companyUM} AS ENERGY_AMOUNT_NIGHT
        FROM
            ANCATE_INFO ai2
            -- 昼間買電量を取得する
            LEFT JOIN ENERGY_USED_RECORD_YEAR_DETAIL eu21 ON (
                eu21.ANCATE_ID = ai2.ANCATE_ID
                AND eu21.ENERGY_ID = 'D04'
            )
            -- 夜間買電量を取得する
            LEFT JOIN ENERGY_USED_RECORD_YEAR_DETAIL eu22 ON (
                eu22.ANCATE_ID = ai2.ANCATE_ID
                AND eu22.ENERGY_ID = 'D06'
            )
        WHERE
            ai2.ANBUN_RATE_{companyUM} > 0
            AND ai2.REPORT_NENDO = {reportNendo}
            AND (
                eu21.ENERGY_AMOUNT > 0
                OR eu22.ENERGY_AMOUNT > 0
            )
    """


def SELECT_OTHER(companyUM, reportNendo):
    """
    指定会社、報告年度のその他のデータを取得するSQL文
    パラメータ：
        company：会社名略称
        reportNendo：報告年度
    戻り値：
        SQL文
    """
    return f"""
        SELECT * FROM (
            -- 化石燃料その他
            SELECT
                eu.ENERGY_ID,
                eu.ENERGY_NAME,
                eu.REPORT_UNIT,
                eu.ENERGY_AMOUNT,
                eu.EXTERNAL_SUPPLY_FUEL_AMOUNT,
                eu.SALE_SECONDARY_ENERGY_AMOUNT,
                0 AS UNUSED_HEAT_AMOUNT,
                eu.NEW_ENERGY_COEFFICIENT,
                ai.BUILDING_NM,
                ai.INDUSTRIAL_CLASS_CD,
                "" AS HEAT_COMPANY_NM
            FROM ENERGY_USED_RECORD_YEAR_DETAIL eu
            JOIN ANCATE_INFO ai
            ON eu.ANCATE_ID = ai.ANCATE_ID
            WHERE eu.ENERGY_ID = 'A29'
                AND eu.REPORT_NENDO = {reportNendo}
                AND ai.ANBUN_RATE_{companyUM} > 0
            UNION ALL
            -- 都市ガス
            SELECT
                eu.ENERGY_ID,
                ai.GAS_COMPANY_NM AS ENERGY_NAME,
                eu.REPORT_UNIT,
                eu.ENERGY_AMOUNT,
                eu.EXTERNAL_SUPPLY_FUEL_AMOUNT,
                eu.SALE_SECONDARY_ENERGY_AMOUNT,
                0 AS UNUSED_HEAT_AMOUNT,
                eu.NEW_ENERGY_COEFFICIENT,
                ai.BUILDING_NM,
                ai.INDUSTRIAL_CLASS_CD,
                "" AS HEAT_COMPANY_NM
            FROM ENERGY_USED_RECORD_YEAR_DETAIL eu
            JOIN ANCATE_INFO ai
            ON eu.ANCATE_ID = ai.ANCATE_ID
            WHERE eu.ENERGY_ID = 'A28'
                AND eu.REPORT_NENDO = {reportNendo}
                AND ai.ANBUN_RATE_{companyUM} > 0
            UNION ALL
            SELECT
                eu.ENERGY_ID,
                eu.ENERGY_NAME,
                eu.REPORT_UNIT,
                eu.ENERGY_AMOUNT,
                eu.EXTERNAL_SUPPLY_FUEL_AMOUNT,
                eu.SALE_SECONDARY_ENERGY_AMOUNT,
                0 AS UNUSED_HEAT_AMOUNT,
                eu.NEW_ENERGY_COEFFICIENT,
                ai.BUILDING_NM,
                ai.INDUSTRIAL_CLASS_CD,
                "" AS HEAT_COMPANY_NM
            FROM ENERGY_USED_RECORD_YEAR_DETAIL  eu
            JOIN ANCATE_INFO ai
            ON eu.ANCATE_ID = ai.ANCATE_ID
            WHERE eu.ENERGY_ID = 'B17'
                AND eu.REPORT_NENDO = {reportNendo}
                AND ai.ANBUN_RATE_{companyUM} > 0
            UNION ALL
            SELECT
                eu.ENERGY_ID,
                CASE
                    WHEN eu.ENERGY_ID = 'C09' THEN SUBSTR(eu.ENERGY_NAME, 1, LENGTH(eu.ENERGY_NAME) - 3)
                    WHEN eu.ENERGY_ID = 'C10' THEN SUBSTR(eu.ENERGY_NAME, 1, LENGTH(eu.ENERGY_NAME) - 4)
                    ELSE eu.ENERGY_NAME
                END AS ENERGY_NAME,
                eu.REPORT_UNIT,
                eu.ENERGY_AMOUNT,
                0 AS EXTERNAL_SUPPLY_FUEL_AMOUNT,
                eu.SALE_SECONDARY_ENERGY_AMOUNT,
                eu.UNUSED_HEAT_AMOUNT,
                eu.NEW_ENERGY_COEFFICIENT,
                ai.BUILDING_NM,
                ai.INDUSTRIAL_CLASS_CD,
                ai.HEAT_COMPANY_NM
            FROM ENERGY_USED_RECORD_YEAR_DETAIL eu
            JOIN ANCATE_INFO ai
                ON eu.ANCATE_ID = ai.ANCATE_ID
            WHERE eu.ENERGY_ID IN ('C09', 'C10')
                AND eu.REPORT_NENDO = {reportNendo}
                AND ai.ANBUN_RATE_{companyUM} > 0

            UNION ALL
            SELECT
                eu.ENERGY_ID,
                eu.ENERGY_NAME,
                eu.REPORT_UNIT,
                eu.ENERGY_AMOUNT,
                0 AS EXTERNAL_SUPPLY_FUEL_AMOUNT,
                eu.SALE_SECONDARY_ENERGY_AMOUNT,
                eu.UNUSED_HEAT_AMOUNT,
                eu.NEW_ENERGY_COEFFICIENT,
                ai.BUILDING_NM,
                ai.INDUSTRIAL_CLASS_CD,
                "" AS HEAT_COMPANY_NM
            FROM ENERGY_USED_RECORD_YEAR_DETAIL eu
            JOIN ANCATE_INFO ai
            ON eu.ANCATE_ID = ai.ANCATE_ID
            WHERE eu.ENERGY_ID = 'C15'
                AND eu.REPORT_NENDO = {reportNendo}
                AND ai.ANBUN_RATE_{companyUM} > 0
            UNION ALL
            SELECT
                CASE WHEN eu.ENERGY_ID = "D26" THEN "D24"
                    ELSE eu.ENERGY_ID
                END AS ENERGY_ID,
                eu.ENERGY_NAME,
                eu.REPORT_UNIT,
                eu.ENERGY_AMOUNT,
                0 AS EXTERNAL_SUPPLY_FUEL_AMOUNT,
                eu.SALE_SECONDARY_ENERGY_AMOUNT,
                0 AS UNUSED_HEAT_AMOUNT,
                eu.NEW_ENERGY_COEFFICIENT,
                ai.BUILDING_NM,
                ai.INDUSTRIAL_CLASS_CD,
                CAST(eu2.ENERGY_AMOUNT AS STRING) AS HEAT_COMPANY_NM
            FROM ENERGY_USED_RECORD_YEAR_DETAIL eu
            JOIN ANCATE_INFO ai
                ON eu.ANCATE_ID = ai.ANCATE_ID
            -- 当該自家発電の設備容量を取得するため
            LEFT JOIN ENERGY_USED_RECORD_YEAR_DETAIL eu2
                ON (eu2.ANCATE_ID = ai.ANCATE_ID
                AND ((eu.ENERGY_ID = "D24" AND eu2.ENERGY_ID = "D25")
                    OR (eu.ENERGY_ID = "D26" AND eu2.ENERGY_ID = "D27")
                )
                )
            WHERE eu.ENERGY_ID IN ('D24', 'D26')
                AND eu.REPORT_NENDO = {reportNendo}
                AND ai.ANBUN_RATE_{companyUM} > 0
        ) sub
        ORDER BY BUILDING_NM, ENERGY_NAME
    """


def SELECT_SHIYORYO(companyUM, reportNendo):
    """
    指定会社、報告年度の各エネルギーの使用量と熱量を取得するSQL文を取得する
    パラメータ：
        company：会社名略称
        reportNendo：報告年度
    戻り値：
        SQL文
    """
    return f"""
        select
            A.REPORT_NENDO
            ,E.ENERGY_ID
            ,ROUND(SUM(E.ENERGY_AMOUNT * A.ANBUN_RATE_{companyUM})) as SHIYORYO
            ,ROUND(SUM(E.ENERGY_AMOUNT * A.ANBUN_RATE_{companyUM} * E.NEW_ENERGY_COEFFICIENT)) as SHIYORYO_GJ
            ,ROUND(SUM(E.ENERGY_AMOUNT * A.ANBUN_RATE_{companyUM} * E.OLD_ENERGY_COEFFICIENT)) as SHIYORYO_GJ_2023
            ,ROUND(SUM(E.EXTERNAL_SUPPLY_FUEL_AMOUNT * A.ANBUN_RATE_{companyUM})) as KYOKYURYO
            ,ROUND(SUM(E.EXTERNAL_SUPPLY_FUEL_AMOUNT * A.ANBUN_RATE_{companyUM} * E.NEW_ENERGY_COEFFICIENT)) as KYOKYURYO_GJ
            ,ROUND(SUM(E.EXTERNAL_SUPPLY_FUEL_AMOUNT * A.ANBUN_RATE_{companyUM} * E.OLD_ENERGY_COEFFICIENT)) as KYOKYURYO_GJ_2023
            ,ROUND(SUM(E.SALE_SECONDARY_ENERGY_AMOUNT * A.ANBUN_RATE_{companyUM})) as HANBAIRYO
            ,ROUND(SUM(E.SALE_SECONDARY_ENERGY_AMOUNT * A.ANBUN_RATE_{companyUM} * E.NEW_ENERGY_COEFFICIENT)) as HANBAIRYO_GJ
            ,ROUND(SUM(E.SALE_SECONDARY_ENERGY_AMOUNT * A.ANBUN_RATE_{companyUM} * E.OLD_ENERGY_COEFFICIENT)) as HANBAIRYO_GJ_2023
            ,ROUND(SUM(E.UNUSED_HEAT_AMOUNT * A.ANBUN_RATE_{companyUM})) as MIRIYORYO
            ,ROUND(SUM(E.UNUSED_HEAT_AMOUNT * A.ANBUN_RATE_{companyUM} * E.NEW_ENERGY_COEFFICIENT)) as MIRIYORYO_GJ
            ,ROUND(SUM(E.UNUSED_HEAT_AMOUNT * A.ANBUN_RATE_{companyUM} * E.OLD_ENERGY_COEFFICIENT)) as MIRIYORYO_GJ_2023

        from ANCATE_INFO A
          left join (
                select
                    case when ENERGY_ID in ("D03", "D04", "D06") then "D01"
                    else ENERGY_ID
                    end as ENERGY_ID                -- 昼間買電と夜間買電のエネルギーIDは違うけど、今年は同じ項目に出力する
                    ,ANCATE_ID
                    ,ENERGY_AMOUNT
                    ,EXTERNAL_SUPPLY_FUEL_AMOUNT
                    ,SALE_SECONDARY_ENERGY_AMOUNT
                    ,UNUSED_HEAT_AMOUNT
                    ,NEW_ENERGY_COEFFICIENT
                    ,OLD_ENERGY_COEFFICIENT
                from
                    ENERGY_USED_RECORD_YEAR_DETAIL
              union all
                 select
                    case ENERGY_ID
                      when "C01" then "C0102"
                      when "C02" then "C0102"
                      when "C03" then "C0304"
                      when "C04" then "C0304"
                      when "C05" then "C0506"
                      when "C06" then "C0506"
                      when "C07" then "C0708"
                      when "C08" then "C0708"
                      when "D10" then "D1011"
                      when "D11" then "D1011"
                    else ENERGY_ID
                    end as ENERGY_ID                -- 調査表には「化石分」と「非化石分」分けるけど、特定表には合計値が必要
                    ,ANCATE_ID
                    ,ENERGY_AMOUNT
                    ,EXTERNAL_SUPPLY_FUEL_AMOUNT
                    ,SALE_SECONDARY_ENERGY_AMOUNT
                    ,UNUSED_HEAT_AMOUNT
                    ,NEW_ENERGY_COEFFICIENT
                    ,OLD_ENERGY_COEFFICIENT
                from
                    ENERGY_USED_RECORD_YEAR_DETAIL
                where
                    ENERGY_ID in ("C01", "C02", "C03", "C04", "C05", "C06", "C07", "C08", "D10", "D11")
           ) E
            on A.ANCATE_ID = E.ANCATE_ID
        where A.REPORT_NENDO = {reportNendo}
          and A.ANBUN_RATE_{companyUM} > 0

        group by A.REPORT_NENDO, E.ENERGY_ID
    """


SELECT_SHIYORYO_RESULT = namedtuple(
    "SELECT_SHIYORYO_RESULT",
    [
        "REPORT_NENDO",
        "ENERGY_ID",
        "SHIYORYO",
        "SHIYORYO_GJ",
        "SHIYORYO_GJ_2023",
        "KYOKYURYO",
        "KYOKYURYO_GJ",
        "KYOKYURYO_GJ_2023",
        "HANBAIRYO",
        "HANBAIRYO_GJ",
        "HANBAIRYO_GJ_2023",
        "MIRIYORYO",
        "MIRIYORYO_GJ",
        "MIRIYORYO_GJ_2023",
    ],
)


def SELECT_NETSURYO(companyUM, reportNendo):
    """
    特定表入力ツールの「燃料・熱」シートのデータ出力ため、
    関連のデータを取得する。

    Args:
        companyUM (String): 会社名略称
        reportNendo (Numbers): 報告年度
    """
    return f"""
        SELECT
            'AB' AS id,
            sum(
                eu.ENERGY_AMOUNT * eu.NEW_ENERGY_COEFFICIENT * em.CO2_EMISSION_FACTOR* ai.ANBUN_RATE_{companyUM}
            ) * 44 / 12  AS value,
            sum(
                eu.SALE_SECONDARY_ENERGY_AMOUNT * eu.NEW_ENERGY_COEFFICIENT * em.CO2_EMISSION_FACTOR* ai.ANBUN_RATE_{companyUM}
            ) * 44 / 12 AS hanbai_value
        FROM
            ENERGY_USED_RECORD_YEAR_DETAIL eu
            JOIN ANCATE_INFO ai ON (eu.ANCATE_ID = ai.ANCATE_ID)
            JOIN ENERGY_MST em ON (
                em.ENERGY_ID = eu.ENERGY_ID
                AND em.NENDO = eu.REPORT_NENDO
            )
        WHERE
            em.ENERGY_TYPE_CD IN ('A', 'B')
            AND em.OTHER_FLG = 0
            AND eu.REPORT_NENDO = {reportNendo}
            AND ai.ANBUN_RATE_{companyUM} > 0
        UNION
        -- 熱
        SELECT
            sub.id,
            SUM(sub.value) AS value,
            SUM(sub.hanbai_value) AS hanbai_value
        FROM
            (
                SELECT
                    CASE
                        WHEN eu.ENERGY_ID IN ('C01', 'C02') THEN 'C0102'
                        WHEN eu.ENERGY_ID IN ('C03', 'C04') THEN 'C0304'
                        WHEN eu.ENERGY_ID IN ('C05', 'C06') THEN 'C0506'
                        WHEN eu.ENERGY_ID IN ('C07', 'C08') THEN 'C0708'
                        ELSE eu.ENERGY_ID
                    END AS id,
                    eu.ENERGY_AMOUNT * eu.NEW_ENERGY_COEFFICIENT * ai.ANBUN_RATE_{companyUM} AS value,
                    eu.SALE_SECONDARY_ENERGY_AMOUNT * eu.NEW_ENERGY_COEFFICIENT * ai.ANBUN_RATE_{companyUM} AS hanbai_value
                FROM
                    ENERGY_USED_RECORD_YEAR_DETAIL eu
                    JOIN ANCATE_INFO ai ON (eu.ANCATE_ID = ai.ANCATE_ID)
                    JOIN ENERGY_MST em ON (
                        em.ENERGY_ID = eu.ENERGY_ID
                        AND em.NENDO = eu.REPORT_NENDO
                    )
                WHERE
                    em.ENERGY_TYPE_CD IN ('C')
                    AND em.OTHER_FLG = 0
                    AND eu.REPORT_NENDO = {reportNendo}
                    AND ai.ANBUN_RATE_{companyUM} > 0
            ) sub
        GROUP BY
            sub.id;

    """


def SELECT_SAIBUNRUI_NETSURYO(companyUM, reprotNendo):
    """産業細分類ごとの燃料・熱情報を取得する

    Args:
        companyUM (String): 会社名略称
        reportNendo (Numbers): 報告年度
    """
    return f"""
        WITH sub AS (
            SELECT
                a.INDUSTRIAL_CLASS_CD
                ,a.ANBUN_RATE_{companyUM}
                ,CASE
                    WHEN eu.ENERGY_ID IN ('C01', 'C02') THEN 'C0102'
                    WHEN eu.ENERGY_ID IN ('C03', 'C04') THEN 'C0304'
                    WHEN eu.ENERGY_ID IN ('C05', 'C06') THEN 'C0506'
                    WHEN eu.ENERGY_ID IN ('C07', 'C08') THEN 'C0708'
                    ELSE eu.ENERGY_ID
                END AS ENERGY_ID
                ,eu.ENERGY_AMOUNT
                ,eu.SALE_SECONDARY_ENERGY_AMOUNT
                ,em.CONVERSION_COEFFICIENT
                ,em.CO2_EMISSION_FACTOR
                ,em.ENERGY_TYPE_CD
                ,em.OTHER_FLG
            FROM
                ANCATE_INFO a
                JOIN ENERGY_USED_RECORD_YEAR_DETAIL eu
                ON (eu.ANCATE_ID = a.ANCATE_ID)
                JOIN ENERGY_MST em
                ON (
                    em.ENERGY_ID = eu.ENERGY_ID
                    AND em.NENDO = a.REPORT_NENDO
                )
            WHERE
                a.REPORT_NENDO = {reprotNendo}
                AND a.ANBUN_RATE_{companyUM} > 0
        )
        -- その他以外の燃料(化石＋非化石)のCO2排出量を取得
        SELECT
            sub_nr.INDUSTRIAL_CLASS_CD
            ,'AB' AS ENERGY_ID
            ,SUM(sub_nr.ENERGY_AMOUNT * sub_nr.ANBUN_RATE_{companyUM} *
                sub_nr.CONVERSION_COEFFICIENT * sub_nr.CO2_EMISSION_FACTOR * 44 / 12) AS USED
            ,SUM(sub_nr.SALE_SECONDARY_ENERGY_AMOUNT * sub_nr.ANBUN_RATE_{companyUM} *
                sub_nr.CONVERSION_COEFFICIENT * sub_nr.CO2_EMISSION_FACTOR * 44 / 12) AS SOLD
        FROM
            sub sub_nr
        WHERE
            sub_nr.ENERGY_TYPE_CD IN ('A', 'B') -- 燃料
            AND sub_nr.OTHER_FLG = 0 -- その他以外
        GROUP BY
            sub_nr.INDUSTRIAL_CLASS_CD
        UNION
        -- その他以外の熱の使用量を取得
        SELECT
            sub_nt.INDUSTRIAL_CLASS_CD
            ,sub_nt.ENERGY_ID
            ,SUM(sub_nt.ENERGY_AMOUNT * sub_nt.ANBUN_RATE_{companyUM}) AS USED
            ,SUM(sub_nt.SALE_SECONDARY_ENERGY_AMOUNT * sub_nt.ANBUN_RATE_{companyUM}) AS SOLD
        FROM
            sub sub_nt
        WHERE
            sub_nt.ENERGY_TYPE_CD = 'C' -- 熱
            AND sub_nt.OTHER_FLG = 0 -- その他以外
        GROUP BY
            sub_nt.INDUSTRIAL_CLASS_CD
            ,sub_nt.ENERGY_ID
    """


SELECT_SAIBUNRUI_NETSURYO_RESULT = namedtuple(
    "SELECT_SAIBUNRUI_NETSURYO_RESULT",
    [
        "INDUSTRIAL_CLASS_CD",
        "ENERGY_ID",
        "USED",
        "SOLD",
    ],
)


def SELECT_GENTANI(companyUM, reportNendo):
    """
    指定会社、報告年度の事業者の全体及び事業分類ごとのエネルギー消費原単位等及び電気需要最適化評価原単位等のデータを取得するSQL文
    パラメータ：
        company：会社名略称
        reportNendo：報告年度
    戻り値：
        SQL文
    """
    return f"""
        SELECT
            AI0.INDUSTRIAL_CLASS_CD,
            AI0.DENOMINATOR_TYPE,
            MAX(
                SUBSTR(KM.KBN_NAME, 1, INSTR(KM.KBN_NAME, '[') - 1)
            ) AS DENOMINATOR_NM,
            MAX(
                SUBSTR(
                    KM.KBN_NAME,
                    INSTR(KM.KBN_NAME, '[') + 1,
                    INSTR(KM.KBN_NAME, ']') - INSTR(KM.KBN_NAME, '[') - 1
                )
            ) AS DENOMINATOR_TANI,
            -- hiveの場合： REGEXP_EXTRACT(KM.KBN_NAME, '\\[(.*?)\\]', 1)
            SUM(AI0.DENOMINATOR_VALUE) AS DENOMINATOR_VALUE,
            ROUND(SUM(
                CASE
                    WHEN SUB.DATA_FLG = 1 THEN 0
                    WHEN SUB.ENERGY_ID IN ('D02', 'D05') THEN 0
                    ELSE SUB.ENERGY_AMOUNT_GJ
                END * AI0.ANBUN_RATE_{companyUM}
            ) * 0.0258) AS A,
            ROUND(SUM(
                CASE
                    WHEN SUB.DATA_FLG = 1 THEN 0
                    WHEN SUB.ENERGY_ID IN ('D02', 'D05') THEN 0
                    ELSE SUB.ENERGY_AMOUNT_GJ_2023
                END * AI0.ANBUN_RATE_{companyUM}
            ) * 0.0258) AS A_2023,
            ROUND(SUM(
                CASE
                    WHEN SUB.DATA_FLG = 1 THEN 0
                    WHEN SUB.ENERGY_ID IN ('D02', 'D05') THEN 0
                    WHEN EM.ENERGY_TYPE_CD = 'B' THEN SUB.ENERGY_AMOUNT_GJ * 0.8
                    ELSE SUB.ENERGY_AMOUNT_GJ
                END * AI0.ANBUN_RATE_{companyUM}
            ) * 0.0258) AS A2,
            ROUND(SUM(
                CASE
                    WHEN SUB.DATA_FLG = 1 THEN 0
                    WHEN SUB.ENERGY_ID IN ('D02', 'D05') THEN 0
                    ELSE SUB.ENERGY_AMOUNT_GJ_2023
                END * AI0.ANBUN_RATE_{companyUM}
            ) * 0.0258) AS A2_2023,
            --販売した副生エネルギーの量(原油換算kl)
            ROUND(SUM(
                CASE
                    WHEN SUB.DATA_FLG = 1 THEN 0
                    WHEN SUB.ENERGY_ID IN ('D02', 'D05') THEN 0
                    ELSE SALE_SECONDARY_ENERGY_AMOUNT_GJ
                END * AI0.ANBUN_RATE_{companyUM}
            ) * 0.0258) AS B,
            ROUND(SUM(
                CASE
                    WHEN SUB.DATA_FLG = 1 THEN 0
                    WHEN SUB.ENERGY_ID IN ('D02', 'D05') THEN 0
                    ELSE SALE_SECONDARY_ENERGY_AMOUNT_GJ_2023
                END * AI0.ANBUN_RATE_{companyUM}
            ) * 0.0258) AS B_2023,
            --購入した未利用熱の量（原油換算kl)
            ROUND(SUM(
                CASE
                    WHEN EM.ENERGY_TYPE_CD <> 'C' THEN 0
                    WHEN SUB.DATA_FLG = 1 THEN 0
                    WHEN SUB.ENERGY_ID IN ('D02', 'D05') THEN 0
                    ELSE UNUSED_HEAT_AMOUNT_GJ
                END * AI0.ANBUN_RATE_{companyUM}
            ) * 0.0258) AS B2,
            ROUND(SUM(
                CASE
                    WHEN EM.ENERGY_TYPE_CD <> 'C' THEN 0
                    WHEN SUB.DATA_FLG = 1 THEN 0
                    WHEN SUB.ENERGY_ID IN ('D02', 'D05') THEN 0
                    ELSE UNUSED_HEAT_AMOUNT_GJ_2023
                END * AI0.ANBUN_RATE_{companyUM}
            ) * 0.0258) AS B2_2023,
            -- 電気需要最適化及び非化石燃料の補正を踏まえたエネルギーの使用量（原油換算kl）
            ROUND(SUM(
                CASE
                    WHEN SUB.DATA_FLG = 0
                        AND SUB.ENERGY_ID IN ('D01', 'D03', 'D04', 'D06', 'D07', 'D08') THEN 0
                    WHEN SUB.ENERGY_ID IN ('D02', 'D05') THEN 0
                    WHEN EM.ENERGY_TYPE_CD = 'B' THEN SUB.ENERGY_AMOUNT_GJ * 0.8
                    ELSE SUB.ENERGY_AMOUNT_GJ
                END * AI0.ANBUN_RATE_{companyUM}
            ) * 0.0258) AS HEIJYUNKA_A2,
            ROUND(SUM(
                CASE
                    WHEN SUB.DATA_FLG = 1 THEN 0
                    WHEN SUB.ENERGY_ID IN ('D02', 'D05') THEN SUB.ENERGY_AMOUNT_GJ_2023 * 0.3
                    ELSE SUB.ENERGY_AMOUNT_GJ_2023
                END * AI0.ANBUN_RATE_{companyUM}
            ) * 0.0258) AS HEIJYUNKA_A2_2023
        FROM
            (
                -- 合理化データを取得する
                SELECT
                    EUY.ANCATE_ID,
                    EUY.ENERGY_ID,
                    0 AS DATA_FLG,
                    -- 0:合理化データ　1:最適化データ
                    EUY.ENERGY_AMOUNT * EUY.NEW_ENERGY_COEFFICIENT AS ENERGY_AMOUNT_GJ,
                    EUY.ENERGY_AMOUNT * EUY.OLD_ENERGY_COEFFICIENT AS ENERGY_AMOUNT_GJ_2023,
                    EUY.SALE_SECONDARY_ENERGY_AMOUNT * EUY.NEW_ENERGY_COEFFICIENT AS SALE_SECONDARY_ENERGY_AMOUNT_GJ,
                    EUY.SALE_SECONDARY_ENERGY_AMOUNT * EUY.OLD_ENERGY_COEFFICIENT AS SALE_SECONDARY_ENERGY_AMOUNT_GJ_2023,
                    EUY.UNUSED_HEAT_AMOUNT * EUY.NEW_ENERGY_COEFFICIENT AS UNUSED_HEAT_AMOUNT_GJ,
                    EUY.UNUSED_HEAT_AMOUNT * EUY.OLD_ENERGY_COEFFICIENT AS UNUSED_HEAT_AMOUNT_GJ_2023
                FROM
                    ENERGY_USED_RECORD_YEAR_DETAIL EUY
                    LEFT JOIN KUBUN_MST KM ON (
                        KM.BUNRUI_CD = '0015'
                        AND KM.KBN_CD = EUY.ENERGY_ID
                    )
                WHERE
                    KM.KBN_CD IS NOT NULL
                    OR EUY.ENERGY_ID IN ('D02', 'D05')
                UNION
                -- 最適化電気データを取得する
                SELECT
                    AI.ANCATE_ID,
                    EUM.ENERGY_ID,
                    1 AS DATA_FLG,
                    -- 0:合理化データ　1:最適化データ
                    SUM(
                        EUM.ENERGY_USAGE_AMOUNT / 1000 * RO.REQUIRE_OPTIMIZATION_COEFFICIENT * (
                            CASE
                                AI.SUBSTATION_ENERGY_GRASP_FLAG
                                WHEN 1 THEN AI.SUBSTATION_FLOOR_RATE -- 1:変電所把握不可
                                ELSE 1
                            END
                        )
                    ) AS ENERGY_AMOUNT_GJ,
                    0 AS ENERGY_AMOUNT_GJ_2023,
                    0 AS SALE_SECONDARY_ENERGY_AMOUNT_GJ,
                    0 AS SALE_SECONDARY_ENERGY_AMOUNT_GJ_2023,
                    0 AS UNUSED_HEAT_AMOUNT_GJ,
                    0 AS UNUSED_HEAT_AMOUNT_GJ_2023
                FROM
                    ENERGY_USED_RECORD_MONTH_DETAIL EUM
                    JOIN ANCATE_INFO AI ON (AI.ANCATE_ID = EUM.ANCATE_ID)
                    JOIN REQUIRE_OPTIMIZATION_COEFFICIENT_FOR_MONTH_MST RO ON (
                        RO.POWER_AREA_CD = AI.POWER_AREA_CD
                        AND RO.REPORT_NENDO = AI.REPORT_NENDO
                        AND RO.TARGET_MONTH = EUM.TARGET_MONTH
                    )
                WHERE
                    EUM.ENERGY_ID IN ('D01', 'D03', 'D04', 'D06', 'D07', 'D08')
                GROUP BY
                    AI.ANCATE_ID,
                    EUM.ENERGY_ID
            ) SUB
            JOIN ANCATE_INFO AI0 ON (AI0.ANCATE_ID = SUB.ANCATE_ID)
            JOIN ENERGY_MST EM ON (EM.ENERGY_ID = SUB.ENERGY_ID
                AND EM.NENDO = AI0.REPORT_NENDO
            )
            LEFT JOIN KUBUN_MST KM ON (
                KM.BUNRUI_CD = '0002'
                AND KM.KBN_CD = AI0.DENOMINATOR_TYPE
            )
        WHERE
            AI0.REPORT_NENDO = {reportNendo}
            AND AI0.ANBUN_RATE_{companyUM} > 0
        GROUP BY
            AI0.INDUSTRIAL_CLASS_CD,
            AI0.DENOMINATOR_TYPE

    """


def SELECT_KOJYO(companyUM, reportNendo):
    """
    指定会社、報告年度の指定工場などのデータを取得するSQL文
    パラメータ：
        company：会社名略称
        reportNendo：報告年度
    戻り値：
        SQL文
    """
    return f"""
        SELECT
            TABLE_1
        FROM
           SHITEI_INFO
        WHERE
            SHITEI_INFO.REPORT_NENDO = {reportNendo}
           -- AND SHITEI_INFO.COMPANY_ID = {companyUM}

    """


def SELECT_TOSHIGAS(companyUM, reportNendo):
    """
    指定会社、報告年度の都市ガスのデータを取得するSQL文
    パラメータ：
        company：会社名略称
        reportNendo：報告年度
    戻り値：
        SQL文
    """
    return f"""
        SELECT
            MAX(ai.GAS_COMPANY_NM),
            eu.NEW_ENERGY_COEFFICIENT,
            SUM(eu.ENERGY_AMOUNT* AI.ANBUN_RATE_{companyUM}) AS TOTAL_ENERGY_AMOUNT,
            SUM(eu.EXTERNAL_SUPPLY_FUEL_AMOUNT* AI.ANBUN_RATE_{companyUM}) AS TOTAL_EXTERNAL_SUPPLY_FUEL_AMOUNT,
            SUM(eu.SALE_SECONDARY_ENERGY_AMOUNT* AI.ANBUN_RATE_{companyUM}) AS TOTAL_SALE_SECONDARY_ENERGY_AMOUNT
        FROM
            ENERGY_USED_RECORD_YEAR_DETAIL eu
        JOIN
            ANCATE_INFO ai ON eu.ANCATE_ID = ai.ANCATE_ID
        WHERE
            eu.ENERGY_ID = 'A28'
            AND ai.REPORT_NENDO = {reportNendo}
            AND ai.ANBUN_RATE_{companyUM} > 0
        GROUP BY
            ai.GAS_COMPANY_ID, eu.NEW_ENERGY_COEFFICIENT;

    """


def SELECT_SAITEKIKA_NISSU(companyUM, reportNendo):
    """
    指定会社、報告年度の電気の需要の最適化に資する措置を実施した日数のデータを取得するSQL文
    パラメータ：
        company：会社名略称
        reportNendo：報告年度
    戻り値：
        SQL文
    """
    return f"""
    SELECT
        MAX(DR_DATE)
    FROM
        ANCATE_INFO
    WHERE
        REPORT_NENDO = {reportNendo}
        AND ANBUN_RATE_{companyUM} > 0

    """


def SELECT_SAITEKIKA_DENKIRYO(companyUM, reportNendo):
    """
    指定会社、報告年度の電気需要最適化を踏まえた電気使用量の内訳のデータを取得するSQL文
    パラメータ：
        company：会社名略称
        reportNendo：報告年度
    戻り値：
        SQL文
    """
    return f"""
    SELECT
   --EUM.TARGET_MONTH,
    SUM(
        EUM.ENERGY_USAGE_AMOUNT / 1000 * ANBUN_RATE_{companyUM} * (
            CASE
                AI.SUBSTATION_ENERGY_GRASP_FLAG
                WHEN 1 THEN AI.SUBSTATION_FLOOR_RATE -- 1:変電所把握不可
                ELSE 1
            END
        )
    ) AS ENERGY_AMOUNT,
    SUM(
        EUM.ENERGY_USAGE_AMOUNT / 1000 * RO.REQUIRE_OPTIMIZATION_COEFFICIENT * ANBUN_RATE_{companyUM} * (
            CASE
                AI.SUBSTATION_ENERGY_GRASP_FLAG
                WHEN 1 THEN AI.SUBSTATION_FLOOR_RATE -- 1:変電所把握不可
                ELSE 1
            END
        )
    ) * 0.0258 AS ENERGY_AMOUNT_KL
FROM
    ENERGY_USED_RECORD_MONTH_DETAIL EUM
    JOIN ANCATE_INFO AI ON (AI.ANCATE_ID = EUM.ANCATE_ID)
    JOIN REQUIRE_OPTIMIZATION_COEFFICIENT_FOR_MONTH_MST RO ON (
        RO.POWER_AREA_CD = AI.POWER_AREA_CD
        AND RO.REPORT_NENDO = AI.REPORT_NENDO
        AND RO.TARGET_MONTH = EUM.TARGET_MONTH
    )
WHERE
    EUM.ENERGY_ID IN ('D01', 'D03', 'D04', 'D06', 'D07', 'D08') -- 電気最適化の対象エネルギー
    AND AI.REPORT_NENDO = {reportNendo}
    AND AI.ANBUN_RATE_{companyUM} > 0
GROUP BY
    EUM.TARGET_MONTH
ORDER BY
    (EUM.TARGET_MONTH + 8) % 12 -- 検索結果の月別順番を4月～3月にする
    """
