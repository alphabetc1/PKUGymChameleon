# -*- coding: utf-8
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.common.by import By
import datetime
import time
import random

def get_boot_date(st, ed):
    date = []
    today = datetime.datetime.now()
    offset = datetime.timedelta(days=1)

    for i in range(ed, st - 1, -1):
        boot_day = (today + i * offset).strftime("%Y-%m-%d")
        date.append(boot_day)

    return date

class Counter:
    driver = None
    conf = None

    def __init__(self, driver, conf):
        self.driver = driver
        self.conf = conf
        print('Driver Launched\n')
    

    def run(self):
        print('Running...')
        bootNum = 0
        while bootNum == 0 :
            try:
                self.login()
                bootNum += self.select_and_boot()
                if bootNum != 0 :
                    break
                time.sleep(300 + random.random() * 300)

            except Exception as e:
                print('Error...')
                print(e)
                self.driver.quit()
                break
                

    def login(self, retry = 0):
        print('Logging in...')
        try:
            self.driver.maximize_window()
            self.driver.get("https://epe.pku.edu.cn/venue/pku/Login")
            WebDriverWait(self.driver, 3).until(EC.visibility_of(self.driver.find_element(By.CLASS_NAME, 'loginFlagWrapItem')))
            loginButton = self.driver.find_element(By.CLASS_NAME, 'loginFlagWrapItem')
            loginButton.click()
            # portal login
            WebDriverWait(self.driver, 3).until(EC.url_to_be('https://iaaa.pku.edu.cn/iaaa/oauth.jsp'))
            WebDriverWait(self.driver, 3).until(EC.visibility_of(self.driver.find_element(By.ID, 'user_name')))
            IDBlock = self.driver.find_element(By.ID, 'user_name')
            passwordBlock = self.driver.find_element(By.ID, 'password')

            IDBlock.send_keys(self.conf.id)
            passwordBlock.send_keys(self.conf.password)

            loginButton = self.driver.find_element(By.ID, 'logon_button')
            loginButton.click()
            WebDriverWait(self.driver, 3).until(EC.url_to_be('https://epe.pku.edu.cn/venue/PKU/home'))
        except:
            if retry < 3:
                self.login(retry + 1)
            else:
                raise Exception('Login Failed')
        
    def select_and_boot(self):
        self.select()
        print ('Booting...')
        # times = [19, 20, 21, 15, 16, 17, 18, 11, 10]
        cnt = 0
        
        boot_date = get_boot_date(self.conf.date_st, self.conf.date_ed)
 
        for date in boot_date:
            self.driver.find_element(By.CLASS_NAME, 'ivu-icon-ios-calendar-outline').click()
            self.driver.find_element(By.CLASS_NAME, 'ivu-input-with-suffix').send_keys(date)
            self.driver.find_element(By.CLASS_NAME, 'ivu-icon-md-refresh').click()
            page = 0

            while cnt == 0:
                # reserve
                index = 0
                WebDriverWait(self.driver, 3).until(lambda _: len(self.driver.find_elements(By.CLASS_NAME, 'reserveBlock'))>=28)
                reserve_blocks = self.driver.find_elements(By.CLASS_NAME, 'reserveBlock')
                row = 2 if page == 2 else 5

                # for time in self.timesPriority:
                for timeStr in self.conf.timesPriority:
                    time = int(timeStr)
                    start_index = (time - 8) * row
                    for delta in range(row - 1, -1, -1):
                        if reserve_blocks[start_index + delta].get_attribute('class').find('free') != -1:
                            reserve_blocks[start_index + delta].click()
                            self.driver.find_element(By.CLASS_NAME, 'ivu-checkbox-input').click()
                            self.driver.find_elements(By.CLASS_NAME, 'payHandleItem')[1].click()
                            WebDriverWait(self.driver, 3).until(lambda _:len(self.driver.find_elements(By.CLASS_NAME, 'ivu-input-default'))==5)
                            self.driver.find_elements(By.CLASS_NAME, 'ivu-input-default')[0].\
                                    clear()
                            self.driver.find_elements(By.CLASS_NAME, 'ivu-input-default')[0].\
                                    send_keys(self.conf.phone_number)
                            self.driver.find_elements(By.CLASS_NAME, 'payHandleItem')[1].click()
                            WebDriverWait(self.driver, 3).until(lambda _:len(self.driver.find_elements(By.CLASS_NAME, 'cardPay'))>0)
                            self.driver.find_elements(By.CLASS_NAME, 'cardPay')[0].click()
                            self.driver.find_elements(By.CLASS_NAME, 'ivu-btn')[1].click()
                            cnt += 1
                            print('日期:' + date + ' page:' + str(page) + ' 时间:' + str(time) + ' 场地' + str(page * 5 + delta + 1))
                    if cnt != 0:
                        break

                # pull right
                pull_right = len(self.driver.find_elements(By.CLASS_NAME, 'pull-right'))>0
                if pull_right is False:
                    break
                page += 1
                self.driver.find_element(By.CLASS_NAME, 'pull-right').click()

        return cnt


    def select(self):
        print('Selecting...')
        self.driver.find_element(By.CLASS_NAME, 'homeWrap').\
            find_element(By.CLASS_NAME, 'header').\
                find_element(By.CLASS_NAME, 'headerContent').\
                    find_elements(By.CLASS_NAME, 'tabItem')[1].click()
        WebDriverWait(self.driver, 3).until(EC.url_to_be('https://epe.pku.edu.cn/venue/pku/venue-introduce?selectIndex=1'))
        WebDriverWait(self.driver, 3).until(EC.visibility_of(self.driver.find_element(By.CLASS_NAME, 'venueList')))
        # venueItem:qdb venueDetailBottomItem:羽毛球场
        self.driver.find_element(By.CLASS_NAME, 'venueList').\
        find_elements(By.CLASS_NAME, 'venueItem')[0].\
            find_element(By.CLASS_NAME, 'venueDetailBottom').\
                find_elements(By.CLASS_NAME, 'venueDetailBottomItem')[0].click() 
        WebDriverWait(self.driver, 3).until(EC.url_to_be('https://epe.pku.edu.cn/venue/pku/venue-reservation/60'))
        # date
        WebDriverWait(self.driver, 3).until(EC.visibility_of(self.driver.find_element(By.CLASS_NAME, 'ivu-icon-ios-calendar-outline')))


    def boot(self):
        print('Booting...')
        

    def count(self):
        print('Counting...')


    def wechat_notification(self):
        print('Wechat Notification...')
        # wechat_notification(userName, sckey)
        # self.conf.wechat, self.conf.sdkey


