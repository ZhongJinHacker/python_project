# -*-coding:utf-8-*-
"""
@author:jiangzhongjin
"""
import pymysql
from config import config as cf


class FsbaseucDatabase:

    def __init__(self):
        config = cf.get_fsbaseuc_config()
        self.conn = pymysql.connect(host=config['host'],
                                    port=config['port'],
                                    user=config['username'],
                                    passwd=config['password'],
                                    db=config['database'])

    def __del__(self):
        self.conn.close()

    def get_user_id(self, company_id, account):
        cursor = self.conn.cursor(pymysql.cursors.DictCursor)
        sql = """
            SELECT
                user_id
            FROM
                uc_user_company
            WHERE
                company_id = '{0}'
                AND
                job_num = '{1}'
            LIMIT 1
        """
        select = sql.format(company_id, account)
        cursor.execute(select)
        user_dict = cursor.fetchone()
        if user_dict is None:
            print('companyId: ' + str(company_id) + ', account: ' + account + '没有对应userId，忽略')
            return None
        return user_dict["user_id"]


fsbaseucDatabase = FsbaseucDatabase()
