import zipfile
import os
from lxml import etree
from middle.common.utils import get_relative_path

twbx_file_path = get_relative_path(r"Tableau\簡易診断_20240620(csv).twbx")

def get_worksheets_from_twbx(twbx_file_path):
    with zipfile.ZipFile(twbx_file_path, 'r') as z:
        # .twb ファイルを見つける
        twb_files = [f for f in z.namelist() if f.endswith('.twb')]
        if not twb_files:
            raise ValueError("No .twb file found in the .twbx archive.")
        
        # 最初の .twb ファイルを解凍して読み込む
        with z.open(twb_files[0]) as f:
            tree = etree.parse(f)
            root = tree.getroot()

            # ワークシート名を抽出
            namespaces = {'t': 'http://tableau.com/api'}
            worksheets = root.xpath('//t:worksheet', namespaces=namespaces)
            worksheet_names = [ws.get('name') for ws in worksheets]
    
    return worksheet_names

# ワークシートの一覧を取得
worksheets = get_worksheets_from_twbx(twbx_file_path)

# ワークシート名を出力
for worksheet in worksheets:
    print(worksheet)
