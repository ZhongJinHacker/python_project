# -*-coding:utf-8-*-
"""
@author:jiangzhongjin
"""
from config import Config
from itms_database import ItmsDatabase
from tdop_database import TdopDatabase
import os

if __name__ == '__main__':
    config = Config()
    tdopDatabase = TdopDatabase(config.get_tdop_config())
    itmsDatabase = ItmsDatabase(config.get_itms_config())
    print('*******')
    doc_name_list = itmsDatabase.get_all_doc_name()
    for doc_name in doc_name_list:
        doc_name_without_suffix = os.path.splitext(doc_name)[0]
        if doc_name_without_suffix:
            position_codes = tdopDatabase.read_position_codes(doc_name_without_suffix)
            if position_codes and len(position_codes) > 0:
                itmsDatabase.update_position_codes_by_doc_name(doc_name, position_codes)


