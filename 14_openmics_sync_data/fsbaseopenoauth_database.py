# -*-coding:utf-8-*-
"""
@author:jiangzhongjin
"""

import pymysql
from config import config as cf


def create_client_model(app_id, secret, company_id):
    client_model = {}
    client_model["id"] = app_id
    client_model["company_id"] = company_id
    client_model["name"] = 'sync'
    client_model["secret"] = secret
    client_model["grant_types"] = '["authorization_code", "refresh_token", "client_credentials"]'
    client_model["response_types"] = '["code", "token"]'
    # client_model["allowed_cors_origins"] = ''
    client_model["redirect_uris"] = '["http://127.0.0.1:3000/callback"]'
    client_model["scopes"] = '["mgc:templatesend", "uninotice:datadispatcher"]'
    client_model["code_expires"] = '600000'
    client_model["token_expires"] = '604800000'
    client_model["refresh_expires"] = '1296000000'
    client_model["creator"] = '-1'
    client_model["updator"] = '-1'
    client_model["create_time"] = '1595227843749'
    client_model["update_time"] = '1595227843749'
    client_model["status"] = '1'
    return client_model


class FsbaseopenoauthDatabase:

    def __init__(self):
        config = cf.get_fsbaseopenoauth_config()
        self.conn = pymysql.connect(host=config['host'],
                                    port=config['port'],
                                    user=config['username'],
                                    passwd=config['password'],
                                    db=config['database'])

    def __del__(self):
        self.conn.close()

    def insert_client(self, client_model):
        cursor = self.conn.cursor()
        sql = """
            INSERT IGNORE INTO
                client
                (id, company_id, name, 
                secret, grant_types, response_types, 
                redirect_uris, scopes, code_expires, 
                token_expires, refresh_expires, creator, 
                updator, create_time, update_time, status
                ) 
            VALUES
                ('{0}', '{1}', '{2}', 
                '{3}', '{4}', '{5}', 
                '{6}', '{7}', '{8}',
                '{9}', '{10}', '{11}',
                '{12}', '{13}', '{14}',
                '{15}'
                )
        """
        insert = sql.format(
            client_model["id"], client_model["company_id"], client_model["name"],
            client_model["secret"], client_model["grant_types"], client_model["response_types"],
            client_model["redirect_uris"], client_model["scopes"], client_model["code_expires"],
            client_model["token_expires"], client_model["refresh_expires"], client_model["creator"],
            client_model["updator"], client_model["create_time"], client_model["update_time"],
            client_model["status"]
            )
        cursor.execute(insert)

        self.conn.commit()
        cursor.close()


fsbaseopenoauthDatabase = FsbaseopenoauthDatabase()
