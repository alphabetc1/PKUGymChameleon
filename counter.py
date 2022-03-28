# -*- coding: utf-8
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.common.by import By
import datetime

def get_boot_date():
    date = []
    today = datetime.datetime.now()
    offset = datetime.timedelta(days=1)

    for i in range(3):
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
                self.select_and_boot()
                if self.conf.boot:
                    bootNum = self.boot()
                    if bootNum != 0 & self.conf.wechat:
                        self.wechat_notification()

            except Exception as e:
                print('Error...')
                print(e)
                self.driver.quit()
                

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
        
        boot_date = get_boot_date()
        for date in boot_date:
            self.driver.find_element(By.CLASS_NAME, 'ivu-icon-ios-calendar-outline').click()
            self.driver.find_element(By.CLASS_NAME, 'ivu-input-with-suffix').send_keys(date)
            self.driver.find_element(By.CLASS_NAME, 'ivu-icon-md-refresh').click()

            while True:
                # reserve
                WebDriverWait(self.driver, 3).until(EC.visibility_of(self.driver.find_element(By.CLASS_NAME, 'reserveBtn')))
                self.driver.find_element(By.CLASS_NAME, 'reserveBtn').click()
                

                # pull right
                pull_right = len(self.driver.find_elements(By.CLASS_NAME, 'pull-right'))>0
                if pull_right is False:
                    break
                self.driver.find_element(By.CLASS_NAME, 'pull-right').click()

        return 0


    def select(self):
        print('Selecting...')
        self.driver.find_element(By.CLASS_NAME, 'tabWrap').\
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


