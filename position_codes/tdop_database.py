# -*-coding:utf-8-*-
"""
@author:jiangzhongjin
"""

import pymysql


class TdopDatabase:

    def __init__(self, config):
        # 打开数据库连接
        self.conn = pymysql.connect(host=config['host'],
                                    port=config['port'],
                                    user=config['username'],
                                    passwd=config['password'],
                                    db=config['database'])

    def __del__(self):
        self.conn.close()

    def read_position_codes(self, doc_name):
        # 使用cursor()方法创建一个游标对象
        cursor = self.conn.cursor()
        version = doc_name
        sql = 'SELECT ' \
                'DISTINCT(post_no) ' \
              'FROM ' \
                'tdop_sort_schedule_version ' \
              'WHERE ' \
                'version = %s'
        rows = cursor.execute(sql, version)
        position_code_list = cursor.fetchall()
        position_codes = ','.join([str(x[0]) for x in position_code_list])
        print('doc_name:', doc_name, '  position_codes --->', position_codes)
        cursor.close()
        return position_codes


# if __name__ == '__main__':
#     dataBase = TdopDatabase()
#     dataBase.read_position_codes('020W-1.0.0(1.2)-20180827200000')
