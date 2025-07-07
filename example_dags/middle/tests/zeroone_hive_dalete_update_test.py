from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import subprocess
from airflow.models import Variable
from kubernetes.client import models as k8s
 
pod_config = {
    "pod_override":
    k8s.V1Pod(spec=k8s.V1PodSpec(containers=[
        k8s.V1Container(name="base",
                        resources=k8s.V1ResourceRequirements(
                            limits={
                                "cpu": "500m",
                                "memory": "3G"
                            },
                            requests={
                                "cpu": "500m",
                                "memory": "3G"
                            }))
    ]))
}
 

# DAG定義
default_args = {
    'owner': 'ZeroOne',
    'start_date': datetime(2024, 1, 1),
    'retries': 0,
}

# DAGの設定
dag = DAG(
    'ZeroOne_Hive_Delete_Update_test',
    default_args=default_args,
    schedule_interval=None, 
)

# Load Airflow variable
pw = Variable.get('zeroone_hive_delete_update_test_pw')

# implya をインストールしてHiveに接続するPython関数
def hive():
    # install impyla
    print('Installing impyla...')
    proxy = 'http://t-prx01.ts.tdh.tepcube.jp:80'
    subprocess.run(['pip', 'install', 'impyla','--proxy', proxy], check=True)
    #subprocess.run(['pip', 'install', 'impyla'], check=True)
    print('Install done.')

    from impala.dbapi import connect

    # Connect to HIVE
    conn = connect(host='t-df04.ts.tdh.tepcube.jp', port=10000, use_ssl=True, user='mapr', password=pw, auth_mechanism='PLAIN')

    cursor = conn.cursor()
    #query = 'SHOW DATABASES'
    #cursor.execute(query)

    #for result in cursor.fetchall():
    #    print(result)

    print('Create zeroone_test database.')
    query = 'CREATE DATABASE IF NOT EXISTS zeroone_test'
    cursor.execute(query)
    #for result in cursor.fetchall():
    #    print(result)

    print('Drop zeroone_test.transaction_test table.')
    query = 'DROP TABLE IF EXISTS zeroone_test.transaction_test PURGE'
    cursor.execute(query)
    #for result in cursor.fetchall():
    #    print(result)

    print('Create zeroone_test.transaction_test table.')
    query = 'CREATE TABLE IF NOT EXISTS zeroone_test.transaction_test (col1 int, col2 string)\n STORED AS ORC\n TBLPROPERTIES (\'transactional\'=\'true\')'
    #print(query)
    cursor.execute(query)
    #for result in cursor.fetchall():
    #    print(result)

    print('Insert 2 rows.')
    query = 'INSERT INTO zeroone_test.transaction_test VALUES (1, \'test1\')'
    cursor.execute(query)
    #for result in cursor.fetchall():
    #    print(result)

    query = 'INSERT INTO zeroone_test.transaction_test VALUES (2, \'test2\')'
    cursor.execute(query)
    #for result in cursor.fetchall():
    #    print(result)

    print ('Initial rows.')
    query = 'SELECT * FROM zeroone_test.transaction_test'
    cursor.execute(query)
    for result in cursor.fetchall():
        print(result)

    print('Delete 1 row.')
    query = 'DELETE FROM zeroone_test.transaction_test WHERE col1 = 1'
    cursor.execute(query)
    #for result in cursor.fetchall():
    #    print(result)

    print('Row(s) after delete.')
    query = 'SELECT * FROM zeroone_test.transaction_test'
    cursor.execute(query)
    for result in cursor.fetchall():
        print(result)

    print('Update 1 row')
    query = 'UPDATE zeroone_test.transaction_test SET col2 = \'updated\' WHERE col1 = 2'
    cursor.execute(query)
    #for result in cursor.fetchall():
    #    print(result)

    print('Row(s) after update.')
    query = 'SELECT * FROM zeroone_test.transaction_test'
    cursor.execute(query)
    for result in cursor.fetchall():
        print(result)

    cursor.close()
    conn.close()


# PythonOperatorを使用してタスクを定義
hive_task = PythonOperator(
    task_id='hive_task',
    python_callable=hive,
    trigger_rule='one_success',
    dag=dag,
    executor_config=pod_config,
    provide_context=True,
)

hive_task

if __name__ == '__main__':
    dag.cli()

