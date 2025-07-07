# sys.path.append('c:\\Users\\msduser\\cndx_workspace\\esg03\\dags')
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from middle.report_register.register_user import get_user_data, insert_user

insert_user(target_file_name="account_application_form.xlsx")