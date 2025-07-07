import json

from ghg.common.log import MyAppLog, log_writer
from ghg.common.utils import get_relative_path

logger = MyAppLog()


# @log_writer(logger)を追加しないでください、ログが長すぎるため
def edit_json_info_data(a, b, current_path=[]):

    error_occurred = False
    if isinstance(a, dict):
        for key, value in a.items():
            new_path = current_path + [key]
            if isinstance(value, dict) or isinstance(value, list):
                if edit_json_info_data(value, b, new_path):
                    error_occurred = True
            else:
                if convert_value(
                    a,
                    key,
                    value,
                    "$".join(new_path),
                    b,
                ):
                    error_occurred = True
    elif isinstance(a, list):
        for item in a:
            if edit_json_info_data(item, b, current_path):
                error_occurred = True
    return error_occurred


# @log_writer(logger)を追加しないでください、ログが長すぎるため
def convert_value(a, key, value, path_key, b):
    if "required" in b.get(path_key, {}) and (value is None or isinstance(value, str)):
        required_value = b[path_key]["required"]
        if required_value == "○" and (value is None or value == ""):
            print(
                f"■■■Error■■■「{path_key}」が必須項目です。該当データ行は{b[path_key]}"
            )
            logger.info(
                f"■■■Error■■■「{path_key}」が必須項目です。該当データ行は{b[path_key]}"
            )
            return True
    return False


#   if "rounding_digit" in b.get(path_key, {}) and isinstance(value, (int, float)):
#       rounding_digit = b[path_key]["rounding_digit"]
#       if not isinstance(rounding_digit, int) or rounding_digit < 0:
#           print(f"Invalid rounding_digit: {rounding_digit} for key: {path_key}")
#           return
#       try:
#           # decimal.Decimalを使用して四捨五入する際の桁数指定を修正
#           value_as_decimal = Decimal(str(value))
#           rounding_factor = Decimal("1e-{}".format(rounding_digit))
#           rounded_value = value_as_decimal.quantize(
#               rounding_factor, rounding=ROUND_HALF_UP
#           )
#           a[key] = float(rounded_value)
#       except InvalidOperation as e:
#           print(f"Rounding error for {path_key} with value {value}: {e}")


@log_writer(logger)
def check_shitei_info_json(shitei_json_data):

    template_json = get_relative_path("template/shitei_info_json_template.json")
    with open(template_json, "r", encoding="utf-8") as f:
        json_str = json.load(f)

    error_occurred = edit_json_info_data(shitei_json_data, json_str)

    return error_occurred


@log_writer(logger)
def check_tokutei_info_json(tokutei_json_data):

    template_json = get_relative_path("template/tokutei_info_json_template.json")
    with open(template_json, "r", encoding="utf-8") as f:
        json_str = json.load(f)

    error_occurred = edit_json_info_data(tokutei_json_data, json_str)
    return error_occurred
