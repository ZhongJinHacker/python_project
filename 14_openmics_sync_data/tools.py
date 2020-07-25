# -*-coding:utf-8-*-
"""
@author:jiangzhongjin
"""
import uuid


def create_uuid():
    """
    生产uuid
    :return:
    """
    return str(uuid.uuid4()).replace('-', '')


if __name__ == '__main__':
    print(create_uuid())