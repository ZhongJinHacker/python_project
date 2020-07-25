# -*-coding:utf-8-*-
"""
@author:jiangzhongjin
"""
from constants import get_role_code_by_id
from fsbasemics_database import fsbasemicsDatabase
from fsbaseopenoauth_database import fsbaseopenoauthDatabase, create_client_model
from tools import create_uuid


class CertService:

    def handle_developer_cert(self, manager_list):
        for app_manager in manager_list:
            app_id = create_uuid()
            secret = create_uuid()
            app_manager["app_id"] = app_id
            app_manager["secret"] = secret
            app_manager["role_code"] = get_role_code_by_id(app_manager["role_id"])
            cert_id = fsbasemicsDatabase.createCert(app_manager)
            fsbaseopenoauthDatabase.insert_client(create_client_model(app_id, secret, app_manager["company_id"]))
            fsbasemicsDatabase.insert_into_mics_rbac_company_user_role_certificate(app_manager, cert_id)

    def handle_dev_mate_cert(self, normal_list):
        for normal_user in normal_list:
            resource_id = normal_user["resource_id"]
            normal_user["role_code"] = get_role_code_by_id(normal_user["role_id"])
            cert_id = fsbasemicsDatabase.query_cert_id_by(resource_id)
            if cert_id is None:
                print("处理开发伙伴： resource_id： " + resource_id + "查不到对应凭证, 忽略")
                continue
            fsbasemicsDatabase.insert_into_mics_rbac_company_user_role_certificate(normal_user, cert_id)



cert_service = CertService()
