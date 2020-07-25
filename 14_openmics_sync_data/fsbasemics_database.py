# -*-coding:utf-8-*-
"""
@author:jiangzhongjin
"""

import pymysql
from config import config as cf
from constants import get_role_code_by_id
from fsbaseuc_database import fsbaseucDatabase


class FsbasemicsDatabase:

    def __init__(self):
        config = cf.get_fsbasemics_config()
        self.conn = pymysql.connect(host=config['host'],
                                    port=config['port'],
                                    user=config['username'],
                                    passwd=config['password'],
                                    db=config['database'])

    def __del__(self):
        self.conn.close()

    def query_mics_rbac_sys_user(self):
        cursor = self.conn.cursor(pymysql.cursors.DictCursor)
        sql = """
            SELECT
                id, company_id, user_id, user_name, introduce, status, reason
            FROM
                mics_rbac_sys_company_user
        """
        rows = cursor.execute(sql)
        src_dict_list = cursor.fetchall()
        if src_dict_list is None:
            src_dict_list = []
        user_dict_list = list(filter(None, map(self.transform_model, src_dict_list)))
        cursor.close()
        return user_dict_list

    def transform_model(self, src_model):
        user_id = fsbaseucDatabase.get_user_id(src_model["company_id"], src_model["user_id"])
        if user_id is None:
            return None

        dst_model = {
            "company_id": src_model["company_id"],
            "user_id": user_id,
            "account": src_model["user_id"],
            "user_name": src_model["user_name"],
            "introduce": src_model["introduce"],
            "status": src_model["status"],
            "reason": src_model["reason"]
        }
        return dst_model

    def insert_into_mics_rbac_company_user(self, dst_user_dict_list):
        cursor = self.conn.cursor()
        sql = """
            INSERT IGNORE INTO
                mics_rbac_company_user
            (company_id, user_id, account, user_name, introduce, status, reason)
            VALUES
            ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}')
        """
        for user in dst_user_dict_list:
            insert = sql.format(user["company_id"],
                                user["user_id"],
                                user["account"],
                                user["user_name"],
                                user["introduce"],
                                user["status"],
                                user["reason"])
            cursor.execute(insert)

        self.conn.commit()
        cursor.close()

    def query_admin_role_user(self):
        cursor = self.conn.cursor(pymysql.cursors.DictCursor)
        sql = """
            SELECT
                company_id, user_id, role_id, resource_id, resource_name, resource_type
            FROM
                mics_rbac_sys_company_user_role_res
            WHERE
                role_id = 1
        """
        rows = cursor.execute(sql)
        src_dict_list = cursor.fetchall()
        if src_dict_list is None:
            src_dict_list = []
        self.transform_user_id(src_dict_list)
        return src_dict_list

    def transform_user_id(self, src_dict_list):
        cursor = self.conn.cursor(pymysql.cursors.DictCursor)
        sql = """
            SELECT
                user_id
            FROM
                mics_rbac_company_user
            WHERE
                company_id = '{0}' AND account = '{1}'
            LIMIT 1
        """
        for src_dict in src_dict_list:
            select = sql.format(src_dict["company_id"], src_dict["user_id"])
            cursor.execute(select)
            user_dict = cursor.fetchone()
            if user_dict is None:
                print("company_id: " + str(src_dict["company_id"]) + ", account：" + str(src_dict["user_id"])
                      + " 没有对应userId, 忽略")
                src_dict_list.remove(src_dict)
                continue
            src_dict["user_id"] = user_dict["user_id"]

        cursor.close()

    def new_admin_role_user(self, ret_list):
        cursor = self.conn.cursor(pymysql.cursors.DictCursor)
        role_code = get_role_code_by_id(1)
        sql = """
            INSERT IGNORE INTO
                mics_rbac_company_user_role_certificate
                (company_id, user_id, role_code)
            VALUES
                ('{0}', '{1}', '{2}')
        """
        for model in ret_list:
            insert = sql.format(model["company_id"],
                                model["user_id"],
                                role_code)
            cursor.execute(insert)
        self.conn.commit()
        cursor.close()

    def query_platform_role_user(self):
        cursor = self.conn.cursor(pymysql.cursors.DictCursor)
        sql = """
            SELECT
                company_id, user_id, role_id, resource_id, resource_name, resource_type
            FROM
                mics_rbac_sys_company_user_role_res
            WHERE
                role_id = 2
        """
        rows = cursor.execute(sql)
        src_dict_list = cursor.fetchall()
        if src_dict_list is None:
            src_dict_list = []
        self.transform_user_id(src_dict_list)
        cursor.close()
        return src_dict_list

    def new_platform_role_user(self, ret_list):
        cursor = self.conn.cursor(pymysql.cursors.DictCursor)
        role_code = get_role_code_by_id(2)
        sql = """
            INSERT IGNORE INTO
                mics_rbac_company_user_role_certificate
                (company_id, user_id, role_code)
            VALUES
                ('{0}', '{1}', '{2}')
        """
        for model in ret_list:
            insert = sql.format(model["company_id"],
                                model["user_id"],
                                role_code)
            cursor.execute(insert)
        self.conn.commit()
        cursor.close()

    def query_app_manager_user(self):
        role_id = 3
        return self._query_mics_rbac_sys_company_user_role_res_user_by_role_id(role_id)

    def _query_mics_rbac_sys_company_user_role_res_user_by_role_id(self, role_id):
        cursor = self.conn.cursor(pymysql.cursors.DictCursor)
        sql = """
            SELECT
                company_id, user_id as account, resource_id, resource_name, resource_type, role_id
            FROM
                mics_rbac_sys_company_user_role_res
            WHERE
                role_id = '{0}'
                AND
                resource_id is not NULL
                AND
                resource_name is not NULL
                AND
                resource_type is not NULL
        """
        select = sql.format(role_id)
        cursor.execute(select)
        user_list = cursor.fetchall()
        cursor.close()
        if user_list is None:
            return []
        return user_list

    def createCert(self, company_user_role_res_user_model):
        insert_id = self.insert_into_mics_rbac_certificate(company_user_role_res_user_model)
        self.insert_into_mics_rbac_certificate_resource(company_user_role_res_user_model, insert_id)
        return insert_id

    def insert_into_mics_rbac_certificate(self, company_user_role_res_user_model):
        cursor = self.conn.cursor(pymysql.cursors.DictCursor)
        sql = """
            INSERT IGNORE INTO
                mics_rbac_certificate
                (developer, certificate, secret, company_id)
            VALUES
                ('{0}', '{1}', '{2}', '{3}')
        """
        model = company_user_role_res_user_model
        insert = sql.format(model["account"], model["app_id"], model["secret"], model["company_id"])
        cursor.execute(insert)
        insert_id = self.conn.insert_id()
        self.conn.commit()
        cursor.close()
        return insert_id

    def insert_into_mics_rbac_certificate_resource(self, company_user_role_res_user_model, insert_id):
        cursor = self.conn.cursor(pymysql.cursors.DictCursor)
        sql = """
            INSERT IGNORE INTO
                mics_rbac_certificate_resource
                (certificate_id, certificate, resource_id, resource_name, resource_type)
            VALUES
                (%s, %s, %s, %s, %s)
        """
        model = company_user_role_res_user_model
        cursor.execute(sql, (insert_id,
                             model["app_id"],
                             model["resource_id"],
                             model["resource_name"],
                             model["resource_type"]))
        self.conn.commit()
        cursor.close()

    def insert_into_mics_rbac_company_user_role_certificate(self, company_user_role_res_user_model, cert_id):
        cursor = self.conn.cursor(pymysql.cursors.DictCursor)
        sql = """
            INSERT IGNORE INTO
                mics_rbac_company_user_role_certificate
                (company_id, user_id, role_code, certificate_id)
            VALUES
                (%s, %s, %s, %s)
        """
        model = company_user_role_res_user_model
        user_id = self.query_user_id_by(model["company_id"], model["account"])
        if user_id is None:
            return
        cursor.execute(sql, (model["company_id"],
                             user_id,
                             model["role_code"],
                             cert_id))
        self.conn.commit()
        cursor.close()

    def query_user_id_by(self, company_id, account):
        cursor = self.conn.cursor(pymysql.cursors.DictCursor)
        sql = """
            SELECT
                user_id
            FROM
                mics_rbac_company_user
            WHERE
                company_id = %s
                AND
                account = %s
        """
        cursor.execute(sql, (company_id, account))
        user_dict = cursor.fetchone()
        if user_dict is None:
            print('companyId: ' + str(company_id) + ', account: ' + account + '没有对应userId，忽略')
            return None
        return user_dict["user_id"]

    def query_report_manager_user(self):
        role_id = 5
        return self._query_mics_rbac_sys_company_user_role_res_user_by_role_id(role_id)

    def query_app_normal_user(self):
        role_id = 4
        return self._query_mics_rbac_sys_company_user_role_res_user_by_role_id(role_id)

    def query_report_normal_user(self):
        role_id = 6
        return self._query_mics_rbac_sys_company_user_role_res_user_by_role_id(role_id)

    def query_cert_id_by(self, resource_id):
        cursor = self.conn.cursor(pymysql.cursors.DictCursor)
        sql = """
            SELECT
                certificate_id
            FROM
                mics_rbac_certificate_resource
            WHERE
                resource_id = %s 
            LIMIT 1
        """
        cursor.execute(sql, (resource_id))
        model_dict = cursor.fetchone()
        if model_dict is None:
            return None
        return model_dict["certificate_id"]

fsbasemicsDatabase = FsbasemicsDatabase()
