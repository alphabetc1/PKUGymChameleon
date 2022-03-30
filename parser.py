# -*- coding: utf-8
from configparser import ConfigParser


class ConfParser:
    def __init__(self, config):
        conf = ConfigParser()
        conf.read(config, encoding='utf8')
        
        # 用户信息
        self.id, self.password = dict(conf['user']).values()

        # 场地信息
        self.date_st, self.date_ed = conf.getint('date', 'st'), conf.getint('date', 'ed')
        self.times = conf.get('times', 'times')
        self.timesPriority = self.times.split(' ')
        self.wechat, self.sdkey = dict(conf['wechat']).values()
        

if __name__ == '__main__':
    conf = ConfParser('config.ini')