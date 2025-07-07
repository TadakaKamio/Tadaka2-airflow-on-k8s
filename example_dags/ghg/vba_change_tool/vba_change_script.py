import json
import os


from win32com.client import Dispatch


def replace_vba_module():
    config_file = get_relative_path(r"vba_change_tool/conf/variables_for_dev.json")

    with open(config_file, "r", encoding='utf-8') as f:
        data = json.load(f)

    source_dir = data["source_files"]
    target_dir = data["target_files"]

    excute_replace_vba_module(source_dir, target_dir)


def excute_replace_vba_module(source_dir, target_dir):
    # ソースディレクトリからモジュール名とそのVBAコードを取得
    vba_modules = {}
    for filename in os.listdir(source_dir):
        module_name = os.path.splitext(filename)[0]  # 拡張子を除去
        with open(os.path.join(source_dir, filename), 'r', encoding='utf-8') as file:
            vba_modules[module_name] = file.read()

    # ターゲットディレクトリ内のExcelファイルを探索
    for root, dirs, files in os.walk(target_dir):
        for file in files:
            if file.lower().endswith('.xlsm'):
                file_path = os.path.join(root, file)
                try:
                    # Excelアプリケーションの起動
                    excel = Dispatch("Excel.Application")
                    excel.Visible = False  # Excelのウィンドウを非表示に設定
                    wb = excel.Workbooks.Open(file_path)  # ワークブックを開く

                    # 対応するVBAモジュールを更新
                    for module_name, new_code in vba_modules.items():
                        if module_name in [vb.Name for vb in wb.VBProject.VBComponents]:
                            vb_component = wb.VBProject.VBComponents(module_name)
                            vb_component.CodeModule.DeleteLines(1, vb_component.CodeModule.CountOfLines)
                            vb_component.CodeModule.AddFromString(new_code)
                            print(f"Updated module {module_name} in {file_path}")

                    # ワークブックの保存と閉じる
                    wb.Save()
                    wb.Close()
                except Exception as e:
                    print(f"Error updating {file_path}: {str(e)}")
                finally:
                    # Excelアプリケーションを閉じる
                    excel.Quit()


def get_relative_path(file_name):
    """
    指定されたファイル名に対して、プロジェクトルートディレクトリからの相対パスを取得する。

    パラメータ:
        file_name (str): 相対パスを取得したいファイルの名前。

    戻り値:
        str: プロジェクトルートディレクトリからの相対パス。
    """
    # 現在のファイルが存在するディレクトリのパスを取得
    current_dir_path = os.path.dirname(os.path.abspath(__file__))

    # 現在のディレクトリの親ディレクトリのパスを取得
    parent_dir_path = os.path.dirname(current_dir_path)

    # 相対パスを組み立て
    return os.path.join(parent_dir_path, file_name)


def main(**kwargs):
    replace_vba_module()


if __name__ == "__main__":
    main()
