# -*- coding: utf-8
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.common.by import By
from boot_time import *
from urllib.parse import quote
from urllib import request
import datetime
import time
import random
import json
from selenium.webdriver.common.action_chains import ActionChains
import urllib
from verifier import *


class Counter:
    driver = None
    conf = None

    def __init__(self, conf):
        self.conf = conf
        

    def open_drive(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        self.driver = webdriver.Edge(
            options=chrome_options,
            executable_path='./drivers/chromedriver',
            service_args=['--ignore-ssl-errors=true', '--ssl-protocol=TLSv1'])
        print('Driver Launched\n')
            

    def run(self):
        print('Running...')
        bootNum = 0
        while bootNum < 2 :
            try:
                self.open_drive()
                self.login()
                bootNum += self.select_and_boot()
                if bootNum > 2 :
                    break
                print("Try again.")
                seconds = seconds_till_twelve()
                time.sleep(min(120 + random.random() * 60, seconds - 1))

            except Exception as e:
                self.driver.quit()
                print('Error...')
                print(e)
                break
                

    def login(self, retry = 0):
        print('Logging in...')
        try:
            # self.driver.maximize_window()
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
        except Exception as e:
            if retry < 2:
                self.login(retry + 1)
            else:
                print (e)
                raise Exception('Login Failed')
        
    def select_and_boot(self):
        self.select()
        print ('Booting...')
        self.boot_date = get_boot_date(self.conf.date_st, self.conf.date_ed)
        cnt = 0
 
        for date in self.boot_date:
            self.driver.find_element(By.CLASS_NAME, 'ivu-icon-ios-calendar-outline').click()
            self.driver.find_element(By.CLASS_NAME, 'ivu-input-with-suffix').send_keys(date)
            self.driver.find_element(By.CLASS_NAME, 'ivu-icon-md-refresh').click()
            page = 0

            while True:
                # reserve
                WebDriverWait(self.driver, 3).until(lambda _: len(self.driver.find_elements(By.CLASS_NAME, 'reserveBlock'))>=28)
                reserve_blocks = self.driver.find_elements(By.CLASS_NAME, 'reserveBlock')
                # row = 2 if page == 2 else 5
                row = 4

                # for time in self.timesPriority:
                for timeStr in self.conf.timesPriority:
                    time = int(timeStr)
                    start_index = (time - 8) * row
                    for delta in range(row - 1, -1, -1):
                        if reserve_blocks[start_index + delta].get_attribute('class').find('free') != -1:
                            boot_info = '日期:' + date + '\n时间:' + str(time) + '\n场地' + str(page * 5 + delta + 1) +  '\n时长' + str(cnt)
                            reserve_blocks[start_index + delta].click()
                            self.driver.find_element(By.CLASS_NAME, 'ivu-checkbox-input').click()
                            self.driver.find_elements(By.CLASS_NAME, 'payHandleItem')[1].click()
                            WebDriverWait(self.driver, 3).until(lambda _:len(self.driver.find_elements(By.CLASS_NAME, 'ivu-input-default'))==5)
                            self.driver.find_elements(By.CLASS_NAME, 'ivu-input-default')[0].\
                                    send_keys(self.conf.phone_number)
                            self.driver.find_elements(By.CLASS_NAME, 'payHandleItem')[1].click()
                            self.verify()
                            WebDriverWait(self.driver, 3).until(lambda _:len(self.driver.find_elements(By.CLASS_NAME, 'cardPay'))>0)
                            self.driver.find_elements(By.CLASS_NAME, 'cardPay')[0].click()
                            self.driver.find_elements(By.CLASS_NAME, 'ivu-btn')[1].click()
                            cnt = 1000
                            # cnt = self.boot(reserve_blocks, start_index, delta, row)
                            return cnt

                # pull right
                pull_right = len(self.driver.find_elements(By.CLASS_NAME, 'pull-right'))>0
                if pull_right is False:
                    break
                page += 1
                self.driver.find_element(By.CLASS_NAME, 'pull-right').click()

        return cnt


    def select(self):
        print('Selecting...')
        WebDriverWait(self.driver, 3).until(EC.visibility_of(self.driver.find_element(By.CLASS_NAME, 'homeWrap')))
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
                find_elements(By.CLASS_NAME, 'venueDetailBottomItem')[1].click() 
        WebDriverWait(self.driver, 3).until(EC.url_to_be('https://epe.pku.edu.cn/venue/pku/venue-reservation/68'))
        # date
        WebDriverWait(self.driver, 3).until(EC.visibility_of(self.driver.find_element(By.CLASS_NAME, 'ivu-icon-ios-calendar-outline')))        


    def boot(self, reserve_blocks, start_index, delta, row):
        cnt = 0
        reserve_blocks[start_index + delta].click()
        if self.conf.boot_time > 1:
            if (start_index + delta + row < len(reserve_blocks) - 5) & reserve_blocks[start_index + delta + row].get_attribute('class').find('free') != -1:
                reserve_blocks[start_index + delta + row].click()
                cnt += 1
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
        return cnt
        # if self.conf.wechat:
        #     wechat_notification(boot_info, self.conf.sdkey)


    def verify(self):
        print('Verifying...')
        self.save_img()
        distance = img_compute_edge()
        tracks = get_track(distance)
        ans = self.slide(tracks)
        if ans != 1:
            self.verify()


    def save_img(self):
        print('Saving img...')
        left_xpath = '/html/body/div[1]/div/div/div[3]/div[2]/div/div[2]/div[2]/div/div[2]/div/div[2]/div/div/div/img'
        right_xpath = '/html/body/div[1]/div/div/div[3]/div[2]/div/div[2]/div[2]/div/div[2]/div/div[1]/div/img'
        left_img_url = self.driver.find_elements_by_xpath(left_xpath)[0].get_attribute('src')
        right_img_url = self.driver.find_elements_by_xpath(right_xpath)[0].get_attribute('src')
        self.save(left_img_url, 'left')
        self.save(right_img_url, 'right')
    

    def save(self, url, name):
        if url != None:
            data = urllib.request.urlopen(url).read()
            f = open('./pics/' + name + '.png', 'wb')
            f.write(data)  
            f.close()


    def slide(self, tracks):
        print('Sliding...')
        block = self.driver.find_element(By.CLASS_NAME, 'verify-move-block')
        # 鼠标点击并按住不松
        ActionChains(self.driver).move_to_element(block).perform()
        ActionChains(self.driver).click_and_hold(block).perform()
        print('move on')
        for item in tracks:
            ActionChains(self.driver).move_by_offset(xoffset=item, yoffset=random.randint(-1,1)).perform()
        # 稳定一秒再松开
        time.sleep(1)
        ActionChains(self.driver).release(block).perform()
        time.sleep(1)
        # 随机拿开鼠标
        # webdriver.ActionChains(self.driver).move_by_offset(xoffset=random.randint(200, 300), yoffset=random.randint(200, 300)).perform()
        print('succ')
        ans_path = '/html/body/div[1]/div/div/div[3]/div[2]/div/div[2]/div[2]/div/div[2]/div/div[1]/div'
        ans = self.driver.find_element_by_xpath(ans_path)
        if '验证成功' in ans.text:
            return 1

        if '验证失败' in ans.text:
            return 2

        return -1


def wechat_notification(boot_info, sckey):
    with request.urlopen(
            quote('https://sctapi.ftqq.com/' + sckey + '.send?title=场地预约成功&desp=' +
                        boot_info + '\n',
                        safe='/:?=&')) as response:
        response = json.loads(response.read().decode('utf-8'))
        if response['error'] == 'SUCCESS':
            print('微信通知成功！')
        else:
            print(str(response['errno']) + ' error: ' + response['errmsg'])
