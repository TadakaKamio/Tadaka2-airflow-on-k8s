from airflow.models import Variable
import middle.common.utils as utils
import middle.common.constants_colums as constants
import middle.common.log as log

# log用instance
logger = log.MiddleAppLog()

@log.log_writer(logger)
def get_file_list(**kwargs):
    try:
        get_path = Variable.get("middle_download_get_path")
        put_base_path = Variable.get(
            "middle_download_put_base_path")
        put_dir_path = Variable.get("middle_download_put_inputfiles_path")
        proself_base_url = Variable.get(
            "middle_download_proself_base_url")
        ignore_files_dir = Variable.get(
            "middle_download_ignore_files_dir")
        proself_auth = Variable.get(
            "middle_download_proself_auth",
            deserialize_json=True)

        # # ダウンロード済みファイルを格納しているvolume内の一覧を取得
        ls_path = utils.pathjoin(put_base_path, ignore_files_dir)

        logger.debug(f'ダウンロード済みファイルパス : {ls_path}')

        exist_files = utils.ls_volume(ls_path)

        logger.debug(f'ダウンロード済みファイル : {exist_files}')
        # 取得対象フォルダ内の一覧を取得
        file_list = utils.recursive_get_list(proself_base_url, get_path,
                                        proself_auth)

        # file_list(Full Path)のファイル名とexist_files(ファイル名のみ)を比較してfile_listのみにあるfull pathを取得する
        download_list = [
            file for file in file_list
            if file.split('/')[-1] not in exist_files
        ]

        filtered_list = []
        for file_path in download_list:
            if not utils.filter_target_file(file_path.split('/')[-1]):
                filtered_list.append(file_path)

                bank_nm = file_path.split('/')[2]
                company_nm = file_path.split('/')[3]
                
                to_make_dir = utils.pathjoin(put_base_path, put_dir_path, bank_nm, company_nm)
                # maprfs上で「銀行/企業/」のフォルダを作成する
                utils.make_folder(to_make_dir)

    except Exception as e:
        logger.error(f'error in get list area. error message : {e}')
        raise e

    if not hasattr(filtered_list, "__iter__"):
        raise ValueError(
            f'download_list is not iterable. items is : {filtered_list}'
        )

    return filtered_list

def download_files(**kwargs):
    get_path = Variable.get("middle_download_get_path")
    put_dir_path = Variable.get("middle_download_put_inputfiles_path")
    put_masterfiles_path = Variable.get("middle_download_put_masterfiles_path")
    put_base_path = Variable.get(
        "middle_download_put_base_path")
    proself_base_url = Variable.get(
        "middle_download_proself_base_url")
    proself_auth = Variable.get(
        "middle_download_proself_auth",
        deserialize_json=True)

    ti = kwargs['ti']
    download_list = ti.xcom_pull(task_ids='get_file_list')

    # for文でのエラーをエスケープする
    if not hasattr(download_list, "__iter__"):
        raise ValueError(
            f'download_list is not iterable. items is : {download_list}'
        )

    error_messages = []
    for files in download_list:
        try:
            # ファイルをダウンロード
            url = utils.make_proself_url(proself_base_url, files)
        
            local_path = utils.basename(files)
            logger.info('download from proself. url is ' + str(url))
            local_path = utils.get_file(url, local_path, proself_auth)
            
            logger.info(f"proself path確認 {local_path}")
            if local_path.endswith(constants.ExcelExtension.CSV.value):
                # マスタファイル移動
                put_path = utils.pathjoin(put_base_path, put_masterfiles_path, local_path)
                logger.info(f"put_path path確認 {put_path}")
            else:
                parts = files.split('/')
                # /05311_ESG-POC/山梨中銀/東電介護老人ホーム/行員向け入力シート_企業カルテ_山梨中銀_2022_1.xlsm
                bank_nm = parts[-3] # parts[2]
                company_nm = parts[-2] # parts[3]

                put_path = utils.pathjoin(put_base_path, put_dir_path, bank_nm, company_nm, local_path)
                logger.info(f"downloadパス★{put_path}")

            put_out = utils.put_file(local_path, put_path)
            if put_out.returncode != 0:
                msg = f'put_file is failed. file name is {local_path}. put path is {put_path}. stdout is {put_out}'
                logger.error(msg)
                raise Exception(msg)

        except Exception as e:
            err_file_msg = f'error download files : {files}.'
            logger.error(err_file_msg)
            err_msg = f'error message : {e}.'
            logger.error(err_msg)
            error_messages.append({
                'error_file': err_file_msg,
                'error_message': err_msg
            })

        try:
            utils.remove_local_file(local_path)
        except Exception as e:
            msg = f'remove local file is failed. local_path is : {local_path}'
            logger.error(msg)
            raise e

    if error_messages:
        raise Exception(str(error_messages))
