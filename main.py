# -*- coding: utf-8
from parser import ConfParser
from counter import Counter
import sys

def sys_path(browser):
    path = f'./{browser}/bin/'
    if sys.platform.startswith('win'):
        return path + f'{browser}.exe'
    elif sys.platform.startswith('linux'):
        return path + f'{browser}-linux'
    elif sys.platform.startswith('darwin'):
        return path + f'{browser}'
    else:
        raise Exception('暂不支持该系统')

if __name__ == '__main__':
    conf = ConfParser('config.ini')
    grabber = Counter(conf)
    grabber.run()
