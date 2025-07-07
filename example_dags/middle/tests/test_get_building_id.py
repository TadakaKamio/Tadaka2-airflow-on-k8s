import pytest
import pandas as pd
from middle.common.utils import get_relative_path
from middle.report_register.register_abatementCurve.register_abatementCurve_inputdata_Info import (
    get_building_id, 
    insert_area_info,
    building_id_list
)

BLANK = ""

# 複数のテスト関数を指定
test_functions = [
    "test_get_building_id_existing_building_name",
    "test_get_building_id_new_building_name",
    "test_get_building_id_multi_new_building_name",
    "test_get_building_id_no_matching_rows"
]

# pytest.main に渡す引数をリストとして作成
pytest_args = ["-v"] + [f"{__file__}::{func}" for func in test_functions]

pytest.main(pytest_args)

@pytest.fixture
def basic_info_df():
    data = {
        'BANK_CODE': ['0142', '9999'],
        'CORPORATE_NUMBER': ['1234567890124', '9999999999999'],
        'AREA_ID': ['1234567890124001', '9999999999999001'],
        'BUILDING_NAME': ['事業所A', '事業所B'],
        'BUILDING_ID': ['1234567890124001001', '9999999999999001001']
    }
    return pd.DataFrame(data)

@pytest.fixture
def file_partition_dic():
    return {
        'file1': {
            'BANK_CODE': '0142',
            'CORPORATE_NUMBER': '1234567890124',
            'AREA_ID': '1234567890124001'
        }
    }

def test_get_building_id_existing_building_name(file_partition_dic, basic_info_df):
    result = get_building_id('file1', file_partition_dic, '事業所A', basic_info_df)
    assert result == '1234567890124001001'

def test_get_building_id_new_building_name(file_partition_dic, basic_info_df):
    # Clear the global list before running the test
    building_id_list.clear()
    
    result = get_building_id('file1', file_partition_dic, '事業所B', basic_info_df)
    assert result == '1234567890124001002'

def test_get_building_id_multi_new_building_name(file_partition_dic, basic_info_df):
    building_id_list.clear()

    building_1 = get_building_id('file1', file_partition_dic, '事業所B', basic_info_df)
    building_2 = get_building_id('file1', file_partition_dic, '事業所C', basic_info_df)

    assert building_1 == '1234567890124001002'
    assert building_2 == '1234567890124001003'

def test_get_building_id_no_matching_rows():
    file_partition_dic = {
        'file2': {
            'BANK_CODE': '0142',
            'CORPORATE_NUMBER': '1234567890123',
            'AREA_ID': '1234567890123001'
        }
    }
    basic_info_df = pd.DataFrame(columns=['BANK_CODE', 'CORPORATE_NUMBER', 'AREA_ID', 'BUILDING_NAME', 'BUILDING_ID'])
    
    result = get_building_id('file2', file_partition_dic, '事業所A', basic_info_df)
    assert result == '1234567890123001001'
