# -*-coding:utf-8-*-
"""
@author:jiangzhongjin
"""


role_dict_list = [
    {
        "src_role_id": 1,
        "dst_role_code": "SUPER_ADMIN"
    },
    {
        "src_role_id": 2,
        "dst_role_code": "PLATFORM_OPERATOR"
    },
    {
        "src_role_id": 3,
        "dst_role_code": "DEVELOPER"
    },
    {
        "src_role_id": 4,
        "dst_role_code": "DEVELOP_MATE"
    },
    {
        "src_role_id": 5,
        "dst_role_code": "DEVELOPER"
    },
    {
        "src_role_id": 6,
        "dst_role_code": "DEVELOP_MATE"
    }
]


def get_role_code_by_id(id):
    for role_dict in role_dict_list:
        if role_dict["src_role_id"] == id:
            return role_dict["dst_role_code"]