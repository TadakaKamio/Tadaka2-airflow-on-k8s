# sys.path.append('c:\\Users\\msduser\\cndx_workspace\\esg03\\dags')
# sys.path.append('c:\\projects\\develop\\dags')
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

# os.environ["MIDDLE_RUN_MODE"] = "product"
# from middle.report_register.register_inputdata.register_inputdata_info import register_input_data
from middle.common.postgre_connect import Psycopg2Singleton
from middle.report_register.register_inputdata.save_inputdata_info import save_input_data
from middle.report_register.register_inputdata.common_main import main

# register_input_data(None)
# main(name="Alice", age=30, city="Tokyo")
postgre_connect_singleton = Psycopg2Singleton()
# コネクション取得
postgre_conn = postgre_connect_singleton._connection
save_input_data(postgre_conn,None,None)