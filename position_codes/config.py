# -*-coding:utf-8-*-
"""
@author:jiangzhongjin
"""
import json

class Config:

    def __init__(self):
        with open('config.json', 'r') as f:
            self.data = json.load(f)

    def __del__(self):
        self.data = None

    def get_tdop_config(self):
        return self.data['tdop']

    def get_itms_config(self):
        return self.data['itms']


if __name__ == '__main__':
    config = Config()
    print(config.get_tdop_config())
    print("****")
    print(config.get_itms_config())
    print("****")


