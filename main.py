# -*- coding: utf-8
from parser import ConfParser
from gymCounter.counter import Grabber

if __name__ == '__main__':
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Edge(
        options=chrome_options,
        executable_path='/usr/bin/chromedriver',
        service_args=['--ignore-ssl-errors=true', '--ssl-protocol=TLSv1'])
        
    conf = ConfParser('config.ini')

    grabber = Grabber(driver, conf)
    grabber.run()
