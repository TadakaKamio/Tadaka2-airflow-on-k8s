# sys.path.append('c:\\Users\\msduser\\cndx_workspace\\esg03\\dags')
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from middle.common.constants_colums import MasterTable
from middle.report_register.register_public_factor import get_activity_minor_category_data, get_electric_supplier_menu_data, get_industy_classification_mst, insert_public_factor

# 処理対象のシートを `constants.MasterTable` から動的に取得
target_sheets = [
    MasterTable.AMCMST.value,
    MasterTable.MJSIC.value,
    MasterTable.MECF.value,
]

insert_public_factor()
# insert_public_factor(target_sheets)
# get_electric_supplier_menu_data()
# get_industy_classification_mst()
# get_activity_minor_category_data()