CREATE TABLE system_control_master (
    control_id INT,
    parameter_name STRING,
    parameter_value STRING,
    parameter_description STRING,
    parameter_type STRING,
    related_entity STRING,
    related_entity_id INT,
    creation_date TIMESTAMP,
    last_updated TIMESTAMP
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE;

/**
コントロール対象確認
・業務日付
・dagID
・dagスケジュール
・メンテ実施予定日
・セキュリティとアクセス制限
・操作可能dag
・処理の制御
・機能の有効無効制御
 */