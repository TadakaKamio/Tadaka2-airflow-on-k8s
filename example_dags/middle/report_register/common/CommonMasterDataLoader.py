import middle.common.constants_colums as constants
from middle.common.hql_processor import get_master_data

#共有マスタデータ情報取得
class CommonMasterDataLoader:
    _instance = None
    def __new__(cls, *args, **kwargs):
        """マスタデータシングルトンインスタンス"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self, conn):
        self.conn = conn
        import middle.common.utils as utils
        json_config = utils.get_json_config()
        schema_middle = json_config["database_posgre"]["schema_middle"]
        schema_commom = json_config["database_posgre"]["schema_commom"]
        DOT = constants.SpecialChars.DOT.value
        self.ecmst_list = get_master_data(conn, None, 
                                            constants.ECMST_COLUMNS, 
                                            schema_middle + DOT + constants.MasterTable.ECMST.value)
        self.ccmst_list = get_master_data(conn, None, 
                                            constants.CCMST_COLUMNS, 
                                            schema_commom + DOT + constants.MasterTable.CCMST.value)
        # self.jicmst_list = get_master_data(conn, None, 
        #                                     constants.JICMST_COLUMNS, 
        #                                     schema_commom + DOT + constants.MasterTable.JICMST.value)
        self.calmst_list = get_master_data(conn, None, 
                                            constants.CALMST_COLUMNS, 
                                            schema_middle + DOT + constants.MasterTable.CALMST.value)
        # self.kbnmst_list = get_master_data(conn, None, 
        #                                     constants.KBNMST_COLUMNS, 
        #                                     schema_name + DOT + constants.MasterTable.KBNMST.value)
        # self.ecdmst_list = get_master_data(conn, None, 
        #                                     constants.ECDMST_COLUMNS, 
        #                                     schema_name + DOT + constants.MasterTable.ECDMST.value)
        # self.ecemst_list = get_master_data(conn, None, 
        #                                     constants.ECEMST_COLUMNS, 
        #                                     schema_name + DOT + constants.MasterTable.ECEMST.value)
        # self.cmst_list = get_master_data(conn, None, 
        #                                     constants.CMST_COLUMNS, 
        #                                     schema_name + DOT + constants.MasterTable.CMST.value)
        # self.becrmst_list = get_master_data(conn, None, 
        #                                     constants.BECRMST_COLUMNS, 
        #                                     schema_name + DOT + constants.MasterTable.BECRMST.value)

