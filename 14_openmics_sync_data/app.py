# -*-coding:utf-8-*-
"""
@author:jiangzhongjin
"""
from cert_service import cert_service
from fsbasemics_database import fsbasemicsDatabase


def sync_company_user():
    """
    同步用户
    :return:
    """
    dst_user_dict_list = fsbasemicsDatabase.query_mics_rbac_sys_user()
    print("1. 查询原表完毕， 一共 " + str(len(dst_user_dict_list)) + "条数据")
    fsbasemicsDatabase.insert_into_mics_rbac_company_user(dst_user_dict_list)
    print("2. 迁移到新用户表完毕")


def sync_cert_role():
    """
    同步用户凭证角色
    :return:
    """
    sync_admin_role_user()
    sync_platform_role_user()
    sync_developer_user()
    sync_dev_mate_user()


def sync_admin_role_user():
    ret_list = fsbasemicsDatabase.query_admin_role_user()
    print("3. 同步管理员用户， 一共 " + str(len(ret_list)) + "条数据")
    fsbasemicsDatabase.new_admin_role_user(ret_list)
    print("4. 管理员用户同步完毕")


def sync_platform_role_user():
    ret_list = fsbasemicsDatabase.query_platform_role_user()
    print("5. 同步平台运营员用户， 一共 " + str(len(ret_list)) + "条数据")
    fsbasemicsDatabase.new_platform_role_user(ret_list)
    print("6. 平台运营员用户同步完毕")


def sync_developer_user():
    app_manager_list = fsbasemicsDatabase.query_app_manager_user()
    print("7. 同步app管理员用户， 一共 " + str(len(app_manager_list)) + "条数据")
    cert_service.handle_developer_cert(app_manager_list)
    print("8. app管理员用户同步完毕")
    report_manager_list = fsbasemicsDatabase.query_report_manager_user()
    print("9. 同步report管理员用户， 一共 " + str(len(report_manager_list)) + "条数据")
    cert_service.handle_developer_cert(report_manager_list)
    print("10. report管理员用户同步完毕")


def sync_dev_mate_user():
    app_normal_user_list = fsbasemicsDatabase.query_app_normal_user()
    print("11. 同步app参与用户， 一共 " + str(len(app_normal_user_list)) + "条数据")
    cert_service.handle_dev_mate_cert(app_normal_user_list)
    print("12. app参与用户同步完毕")
    report_normal_user_list = fsbasemicsDatabase.query_report_normal_user()
    print("13. 同步report参与用户， 一共 " + str(len(report_normal_user_list)) + "条数据")
    cert_service.handle_dev_mate_cert(report_normal_user_list)
    print("14. report参与用户同步完毕")


if __name__ == '__main__':
    print("迁移开始...")
    sync_company_user()
    sync_cert_role()
    print("迁移完成....")
