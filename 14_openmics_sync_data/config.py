# -*-coding:utf-8-*-
"""
@author:jiangzhongjin
"""
import json
import os

CUR_DIR_PATH = os.path.dirname(os.path.realpath(__file__))

"""
config.json path
"""
CONFIG_PATH = CUR_DIR_PATH + os.sep + 'config.json'


class Config:

    def __init__(self):
        with open(CONFIG_PATH, 'r') as f:
            self.data = json.load(f)

    def __del__(self):
        self.data = None

    def get_fsbasemics_config(self):
        return self.data['fsbasemics']

    def get_fsbaseopenoauth_config(self):
        return self.data['fsbaseopenoauth']

    def get_fsbaseuc_config(self):
        return self.data['fsbaseuc']


config = Config()
