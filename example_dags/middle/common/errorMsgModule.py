import sys, traceback
import middle.common.utils as utils
import middle.common.log as log

logger = log.MiddleAppLog()

def custom_exception_handler(exc_type, exc_value, exc_traceback):
    # エラー情報を出力する
    print("例外が発生しました:")
    print("エラータイプ:", exc_type)
    print("エラーメッセージ:", exc_value)
    print("トレースバック:")
    for tb in traceback.format_tb(exc_traceback):
        print(tb)

# カスタムのエラーハンドラをセットする
sys.excepthook = custom_exception_handler

class ValidationError(Exception):
    """カスタムのバリデーションエラークラス"""
    pass

@log.log_writer(logger)
def validate_data(data):
    """データのバリデーションを行う関数"""
    for item in data:
        # バリデーションルールに従ってデータをチェックする
        if utils.is_empty(item):
            raise ValidationError("必須項目未入力のバリデーションチェックエラーが発生しました。")
        
class ErrorHandler:
    def handle_error(self, error_type, error_message):
        if error_type == "ValueError":
        #if error_type in error_type_list1:
            #バリデーションチェック不正
            self.Validation_check_failure_error(error_message)
        elif error_type == "Resource_not_found":
            #リソース存在しない
            self.Resource_not_found_error(error_message)    
        elif error_type == "Conflict":
            #コンフリクトエラー
            self.Conflict_error(error_message)
        elif error_type == "Incomplete_master_data":
            #マスタデータ不備
            self.Incomplete_master_data_error(error_message)
        elif error_type == "AnalysisException":
            #SQL
            self.error_typeerror_error(error_message)
        #例外追加
        else:
            #システムエラー
            self.System_error(error_message)

    #バリデーションチェック不正
    def Validation_check_failure_error(self,error_message):
        loggerModule.MyAppLog.error(error_message)
        #その他
        
    #リソース存在しない
    def Resource_not_found_error(self,error_message):
        loggerModule.MyAppLog.error(error_message)
        #その他
        
    #コンフリクトエラー  
    def Conflict_error(self,error_message):
        loggerModule.MyAppLog.error(error_message)
        #その他
        
    #マスタデータ不備      
    def Incomplete_master_data_error(self, error_message):
        loggerModule.MyAppLog.error(error_message)
        #その他
        
    #システムエラー
    def System_error(self, error_message):
        loggerModule.MyAppLog.error(error_message)
        #その他

    #SQL    
    def error_typeerror_error(self, error_message):
        loggerModule.MyAppLog.error(error_message)
        #その他
