# -*- coding: utf-8
from parser import ConfParser
from counter import Counter
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
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
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Edge(
        options=chrome_options,
        executable_path='/usr/bin/chromedriver',
        service_args=['--ignore-ssl-errors=true', '--ssl-protocol=TLSv1'])
        
    conf = ConfParser('config.ini')

    grabber = Counter(driver, conf)
    grabber.run()
