import re
import datetime
import pandas as pd

# メインチェック        
def check_main(df, datalist,type):
    '''
    df: 判断のDataFrame
    datalist: 判断用固定係数
    type:　判断種類　
        1:number:　判断：整数長さと小数長さ
        2:mail:  判断：メール
        3:date:  判断：時間年月日
        4:month:  判断：月
        5:fixed: 　判断：固定の長さ
        6:data: 判断：普通データ、一定の長さ以下 
        7:phone: 判断: 10桁の電話のみ、(携帯電話非許可)
        8:test: テスト用
    '''
    #整数長さと小数長さ
    if type == 1 :
        for column_name, Integer_Digits , Fractional_Digits in datalist:
            if column_name in df.columns:
                for index in df.index:
                    try:
                        checkNumber(df, index, column_name, Integer_Digits,Fractional_Digits)
                    except ValueError as e:
                        print(e)
                        
    # メール
    if type == 2:
        for column_name in datalist:
            if column_name in df.columns:
                for item in df[column_name]:
                    try:
                        checkMail(item)
                    except ValueError as e :
                        print(e)
   
    # 時間年月日            
    if type == 3:
        for column_name ,num in datalist:
            if column_name in df.columns:
                for index in df.index:
                    try:
                        chackDate(df,index, column_name ,num)
                    except ValueError as e :
                        print(e)

    # 月
    if type == 4:
        for column_name in datalist:
            if column_name in df.columns:                
                for index in df.index:    
                    try:
                        month_check(df,index, column_name)
                    except ValueError as e :
                        print(e)

    # 固定の長さ  
    index = 0              
    if type == 5:
        for column_name ,num in datalist:
            if column_name in df.columns:
                for item in df[column_name]:
                    try:
                        fixed_length_data_check(item, num)
                    except ValueError as e:
                        index += 1
                        raise RuntimeError(f"Critical error in column '{column_name}', row {index}: {e}") 
 
    # 普通の長さ                    
    if type == 6:
        for column_name ,num in datalist:
            if column_name in df.columns:
                for item in df[column_name]:
                    try:
                        data_check(item,num)     
                    except ValueError as e:
                        print(e)  

    # 電話番号                       
    if type == 7:
        for column_name ,num in datalist:
            if column_name in df.columns:
                for index in df.index:    
                    try:
                        phone_number_check(df,index, column_name)
                    except ValueError as e:
                        print(e)  
    
    # テスト専用線                       
    if type == 8:
        for column_name ,num in datalist:
            if column_name in df.columns:
                for item in df[column_name]:
                    try:
                        test_check(item,num)   
                    except ValueError as e:
                        print(e)       

# 数値データ整数、小数長さチェック
def checkNumber(df,index, column_name, Integer_Digits, Fractional_Digits):
    '''
    df : DataFrame
    index : DataFrame 行数
    column_name　: DataFarme 行名
    Integer_Digits : データ整数部分
    Fractional_Digits : データ小数部分
    '''
    # データ読み込む
    Number = df.at[index, column_name]
    # str化
    if Number is not None and not pd.isna(Number):  
        num_str = str(Number)  
    else:
        num_str = ""    
    # 整数と小数分ける
    if '.' in num_str:
        integer_part, decimal_part = num_str.split('.')
    else:
        integer_part, decimal_part = num_str, ''
    
    # 整数部分超える判断
    if  len(integer_part) > Integer_Digits:
        raise ValueError(f"log:{column_name}->{Number}、{Integer_Digits}位を超えました、再入力してお願いいたします")
    
    # 小数部分整理
    if len(decimal_part) > Fractional_Digits:
        Number = round(Number, Fractional_Digits)

    df.at[index, column_name] = Number

# メールデータチェック
def checkMail(email):
    '''
    email : メールデータ
    '''
    
    # メールの正規
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    
    # メールチェック
    if not re.match(pattern, email):
        raise ValueError("log:Emailエラー")

# 日付長さチェック
def chackDate(df,index, column_name,num):
    '''
    df : DataFrame
    index : DataFrame 行数
    column_name　: DataFarme 行名
    num : 日付データ長さ
    '''
    cleaned_date = None
    #データ読み込む
    date= df.at[index, column_name]
    #Nanの場合
    if date is None and pd.isna(date):
        raise ValueError("log:時間データなし")
    # 日付形式転換
    if isinstance(date, (datetime.date, datetime.datetime)):
        date = date.strftime('%Y%m%d')  
    
    if isinstance(date, str):
        cleaned_date = date.replace('-', '').replace('/', '').replace('.', '').replace(' ', '')
    else:
        cleaned_date = str(date).replace('-', '').replace('/', '').replace('.', '').replace(' ', '')
    
    # 例外：2023-333-333
    if len(cleaned_date) >8 :
        raise ValueError("log:時間モジュール解析できない")
    
    # エラーデータ処理
    # 文字列化
    date_str = str(date)
    # 条件YYYYMMDD or YYYYMM、入力値（1. 2022-1-1,　2. 2022-01-1, 3. 2022-1-12）三種類の修正
    if num in [6,8] and len(cleaned_date) < 8 and len(cleaned_date)>5 :
        
        pattern = r'(\d{4})[-/. ](\d{1,2})[-/. ](\d{1,2})'
        match = re.search(pattern, date_str)
        #　存在する判定
        if match:
            YEAR = match.group(1)
            MONTH = match.group(2)
            DAY = match.group(3)
        else:
            raise ValueError("log:解析できない")
        # "0" 追加
        if len(MONTH) == 1:
            MONTH = "0"+MONTH
        if len(DAY) == 1:
            DAY = "0"+DAY
    
        # 組み合わせ
        cleaned_date = YEAR+ MONTH+DAY
    
    #条件：YYYYMM　入力内容　(2022-1)の修正
    if num == 6 and len(cleaned_date)<6 :
        pattern = r'(\d{4})[-/. ](\d{1,2})'
        match = re.search(pattern, date_str)
        
        if match:
            YEAR = match.group(1)
            MONTH = match.group(2)
        else:
            raise ValueError("log:解析できない")
        
        # "0"追加
        if len(MONTH) == 1:
            MONTH = "0"+MONTH

        # 組み合わせ
        cleaned_date = YEAR+ MONTH
        
    # 日付位数足りない
    if len(cleaned_date) < num:
        raise ValueError("log:日付エラー")
    
    # 日付チェック
    # 条件：YYYY
    if num == 4:
        result = cleaned_date[:4]
        
    # 条件：YYYYMM
    elif num == 6:
        result = cleaned_date[:6]
        x = int(cleaned_date[4:6])
        if x <1 or x > 12:
            raise ValueError("log:日付月別エラー")
        
    # 条件：YYYYMMDD
    elif num == 8:
        result = cleaned_date[:8]
        year = int (cleaned_date[0:4])
        month = int(cleaned_date[4:6])
        day = int(cleaned_date[6:8])
        
        # 1~12月
        if month < 1 or month > 12 :
            raise ValueError("log:日付月別エラー")
        
        # 1,3,5,7,8,10,12 31日
        if month in [1,3,5,7,8,10,12]:
            if day < 1 or day > 31:
                raise ValueError("log:日付日別エラー")
            
        # 4,6,9,11 30日
        elif month in [4,6,9,11] :
            if day < 1 or day > 30 :
                raise ValueError("log:日付日別エラー")
            
        # 2 年度%4 =0 29日　以外は28日
        elif month == 2:
            if year % 4 == 0:
                if day < 1 or day > 29 :
                    raise ValueError("日付日別エラー")
            else :
                if day < 1 or day > 28 :
                    raise ValueError("日付日別エラー")
    
    df.at[index, column_name] = int(result)
    
# 固定長さデータチェック
def fixed_length_data_check(data,num):
    """
    data : 固定長さデータ
    num : データ長さ
    """
    
    if len(data) != num:
        raise ValueError("log:データ長さ足りない")
    if data is None:
        raise ValueError(f"log:データなし ") 


# 普通データ長さチェック    
def data_check(data,num):
    '''
    data : 普通データデータ
    num : データ長さ
    '''
    
    if not isinstance(data, str):
        data_str = str(data)
        
    if len(data_str)>num:
        raise ValueError("log:サイズ長い")

# 月チェック
def month_check (df ,index , column_name):
    '''
    df : DataFrame
    index : DataFrame 行数
    column_name　: DataFarme 行名
    '''
    # データ読み込む
    month = df.at[index, column_name]
    if month is None or pd.isna(month):
        raise RuntimeError("log :データなし") 
    # データint化
    month = int(month)
    if month<1 or month >12:
        raise ValueError("log:月データエラー")
    else:
        month_str =str(month)
        if len(month_str) == 1:
            month_str= "0"+month_str
        
    df.at[index, column_name] = month_str

# 電話番号チェック
def phone_number_check(df ,index , column_name):
    # "-" "　"など 削除
    phone_number = df.at[index, column_name]

    # 0からの合計１０桁の電話番号（携帯電話は非許可）
    pattern = r'^(\+?81|0)\d{1,4}[ \-]?\d{1,4}[ \-]?\d{4}$'
    match  = bool(re.match(pattern, phone_number))
    if not match  :
        raise ValueError(f"log:”{phone_number}”はエラー")     
    
    df.at[index, column_name] = phone_number
    
# テスト用8番
def test_check (data, num) :
    data_str = str(data)
    if len(data_str)>num :
        raise ValueError(f"”{data}”はエラー")   