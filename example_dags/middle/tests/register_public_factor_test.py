import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
from middle.report_register.register_public_factor import insert_public_factor

class TestInsertPublicFactor(unittest.TestCase):

    @patch("middle.report_register.register_public_factor.utils.install_package")
    @patch("middle.report_register.register_public_factor.Variable.get")
    @patch("middle.report_register.register_public_factor.utils.get_file_from_hadoop")
    @patch("middle.report_register.register_public_factor.pd.ExcelFile")
    @patch("middle.report_register.register_public_factor.insert_data")
    @patch("middle.report_register.register_public_factor.ImpalaSingleton")
    def test_insert_public_factor_dev_mode(self, MockImpalaSingleton, mock_insert_data, mock_excel_file, mock_get_file_from_hadoop, mock_variable_get, mock_install_package):
        # モックの設定
        mock_install_package.return_value = None  # install_package の戻り値を無視

        # 必要な戻り値をモック
        mock_variable_get.side_effect = lambda key: "test_value" if key in ["middle_download_put_base_path", "middle_download_put_masterfiles_path"] else None
        mock_get_file_from_hadoop.return_value = {
            "file_path": MagicMock(name="file_path")
        }

        # Excelファイルモック
        mock_file = MagicMock(spec=pd.ExcelFile)
        mock_file.sheet_names = ['Sheet1', 'Sheet2']
        mock_excel_file.return_value = mock_file

        # シート名がマスタテーブルに存在するものと仮定
        mock_master_table_info = {
            'Sheet1': {
                "columns": ['col1', 'col2'],
                "table_name": 'schema_commom.table1'
            },
            'Sheet2': {
                "columns": ['col3', 'col4'],
                "table_name": 'schema_commom.table2'
            }
        }
        with patch.dict("middle.report_register.register_public_factor.constants.MasterTable", mock_master_table_info):
            # 実行
            insert_public_factor(target_sheets=['Sheet1'])

            # insert_dataが呼ばれること
            mock_insert_data.assert_called()

    @patch("middle.report_register.register_public_factor.utils.install_package")
    @patch("middle.report_register.register_public_factor.Variable.get")
    @patch("middle.report_register.register_public_factor.utils.get_file_from_hadoop")
    @patch("middle.report_register.register_public_factor.pd.ExcelFile")
    @patch("middle.report_register.register_public_factor.insert_data")
    def test_insert_public_factor_no_file(self, mock_insert_data, mock_excel_file, mock_get_file_from_hadoop, mock_variable_get, mock_install_package):
        # モックの設定
        mock_install_package.return_value = None  # install_package の戻り値を無視

        # ファイルがない場合のシナリオ
        mock_variable_get.side_effect = lambda key: "test_value" if key in ["middle_download_put_base_path", "middle_download_put_masterfiles_path"] else None
        mock_get_file_from_hadoop.return_value = {}

        # 実行
        result = insert_public_factor(target_sheets=['Sheet1'])

        # insert_dataが呼ばれないこと
        mock_insert_data.assert_not_called()

    @patch("middle.report_register.register_public_factor.utils.install_package")
    @patch("middle.report_register.register_public_factor.Variable.get")
    @patch("middle.report_register.register_public_factor.utils.get_file_from_hadoop")
    @patch("middle.report_register.register_public_factor.pd.ExcelFile")
    @patch("middle.report_register.register_public_factor.insert_data")
    @patch("middle.report_register.register_public_factor.ImpalaSingleton")
    def test_insert_public_factor_prod_mode(self, MockImpalaSingleton, mock_insert_data, mock_excel_file, mock_get_file_from_hadoop, mock_variable_get, mock_install_package):
        # モックの設定
        mock_install_package.return_value = None  # install_package の戻り値を無視

        # 必要な戻り値をモック
        mock_variable_get.side_effect = lambda key: "test_value" if key in ["middle_download_put_base_path", "middle_download_put_masterfiles_path"] else None
        mock_get_file_from_hadoop.return_value = {
            "file_path": MagicMock(name="file_path")  # ダミーファイル
        }

        # Excelファイルモック
        mock_file = MagicMock(spec=pd.ExcelFile)
        mock_file.sheet_names = ['Sheet1', 'Sheet2']  # シート名のリスト
        mock_excel_file.return_value = mock_file

        # シート名がマスタテーブルに存在するものと仮定
        mock_master_table_info = {
            'Sheet1': {
                "columns": ['col1', 'col2'],
                "table_name": 'schema_commom.table1'
            },
            'Sheet2': {
                "columns": ['col3', 'col4'],
                "table_name": 'schema_commom.table2'
            }
        }
        with patch.dict("middle.report_register.register_public_factor.constants.MasterTable", mock_master_table_info):
            # 実行
            insert_public_factor(target_sheets=['Sheet1'])

            # insert_dataが呼ばれること
            mock_insert_data.assert_called()

    def test_insert_public_factor_with_invalid_sheet(self):
        # シート名がマスタテーブルに存在しない場合
        with patch("middle.report_register.register_public_factor.utils.get_file_from_hadoop", return_value={"file_path": MagicMock(name="file_path")}), \
             patch("middle.report_register.register_public_factor.pd.ExcelFile") as mock_excel_file, \
             patch("middle.report_register.register_public_factor.insert_data") as mock_insert_data:

            # ダミーExcelファイル
            mock_excel_file.return_value = MagicMock(spec=pd.ExcelFile)
            mock_excel_file.return_value.sheet_names = ['InvalidSheet']

            # 実行
            insert_public_factor(target_sheets=['InvalidSheet'])

            # insert_dataは呼ばれないこと
            mock_insert_data.assert_not_called()

if __name__ == "__main__":
    unittest.main()
