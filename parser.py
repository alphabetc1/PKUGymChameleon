# -*- coding: utf-8
from configparser import ConfigParser


class ConfParser:
    def __init__(self, config):
        conf = ConfigParser()
        conf.read(config, encoding='utf8')
        
        self.id, self.password = dict(conf['user']).values()

        self.venue = dict(conf['venue']).values()
        self.date = dict(conf['date']).values()
        self.times, self.len = dict(conf['times']).values()
        
        self.wechat, self.sdkey = dict(conf['wechat']).values()