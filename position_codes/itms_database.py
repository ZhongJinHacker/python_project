# -*-coding:utf-8-*-
"""
@author:jiangzhongjin
"""
import pymysql


class ItmsDatabase:

    def __init__(self, config):
        # 打开数据库连接
        self.conn = pymysql.connect(host=config['host'],
                                    port=config['port'],
                                    user=config['username'],
                                    passwd=config['password'],
                                    db=config['database'])

    def __del__(self):
        self.conn.close()

    def get_all_doc_name(self):
        cursor = self.conn.cursor()
        sql = 'SELECT ' \
                'DISTINCT(upload_file_name) ' \
              'FROM ' \
                'tt_transfer_upload_history ' \
              'WHERE ' \
                'position_codes is NULL AND upload_file_name is not NULL'
        rows = cursor.execute(sql)
        object_list = cursor.fetchall()
        doc_name_list = list(map(lambda obj : obj[0], object_list))
        print(len(doc_name_list))
        cursor.close()
        return doc_name_list

    def update_position_codes_by_doc_name(self, doc_name, position_codes):
        cursor = self.conn.cursor()
        sql = "UPDATE tt_transfer_upload_history SET position_codes = '{0}' WHERE upload_file_name = '{1}'"
        update = sql.format(position_codes, doc_name)
        row = cursor.execute(update)
        self.conn.commit()
        cursor.close()


# if __name__ == '__main__':
#     dataBase = ItmsDatabase(config)
#     dataBase.get_all_doc_name()
#     dataBase.update_position_codes_by_doc_name('574W[SH]-1.0.0(1.2)-20190226135807.xlsx', 'GF,LF')
