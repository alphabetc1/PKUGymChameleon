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


class Chameleon:
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
        boot_time = 0
        while boot_time < self.conf.boot_time :
            try:
                self.open_drive()
                self.login()
                boot_time += self.select_and_boot()
                if boot_time >= self.conf.boot_time :
                    break
                print("Try again.")
                seconds = seconds_till_twelve()
                time.sleep(min(120 + random.random() * 60, seconds - 3))
            except Exception as e:
                print('Error...')
                current_time = current_hour_minute_second()
                self.driver.get_screenshot_as_file('./pics/debug_' + current_time + '.png')
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
            if retry < 2:
                self.login(retry + 1)
            else:
                raise Exception('Login Failed')
        

    def select_and_boot(self):
        print ('Booting...')
        rows = []
        if self.conf.boot_place == 1:
            rows = self.select_qdb()
        if self.conf.boot_place == 2:
            rows = self.select_54()
        
        self.boot_date = get_boot_date(self.conf.date_st, self.conf.date_ed)
        cnt = 0
 
        for date in self.boot_date:
            self.driver.find_element(By.CLASS_NAME, 'ivu-icon-ios-calendar-outline').click()
            self.driver.find_element(By.CLASS_NAME, 'ivu-input-with-suffix').send_keys(date)
            self.driver.find_element(By.CLASS_NAME, 'ivu-icon-md-refresh').click()
            page = 0

            for row in rows:
                # reserve
                WebDriverWait(self.driver, 3).until(lambda _: len(self.driver.find_elements(By.CLASS_NAME, 'reserveBlock'))>=28)
                reserve_blocks = self.driver.find_elements(By.CLASS_NAME, 'reserveBlock')

                # for time in self.timesPriority:
                for timeStr in self.conf.timesPriority:
                    time = int(timeStr)
                    start_index = (time - 8) * row
                    for delta in range(row - 1, -1, -1):
                        if reserve_blocks[start_index + delta].get_attribute('class').find('free') != -1:
                            cnt = self.boot(reserve_blocks, start_index, delta, row)
                            boot_info = '日期:' + date + '\n时间:' + str(time) + '\n场地' + str(page * 5 + delta + 1) +  '\n时长' + str(cnt)
                            print(boot_info)
                            if self.conf.wechat:
                                wechat_notification(boot_info, self.conf.sckey)
                            return cnt
                # pull right
                pull_right = len(self.driver.find_elements(By.CLASS_NAME, 'pull-right'))>0
                if pull_right is False:
                    break
                page += 1
                self.driver.find_element(By.CLASS_NAME, 'pull-right').click()

        return cnt


    def select_qdb(self, retry = 0):
        print('Selecting qdb...')
        try:
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
                    find_elements(By.CLASS_NAME, 'venueDetailBottomItem')[0].click() 
            WebDriverWait(self.driver, 3).until(EC.url_to_be('https://epe.pku.edu.cn/venue/pku/venue-reservation/60'))
            # date
            WebDriverWait(self.driver, 3).until(EC.visibility_of(self.driver.find_element(By.CLASS_NAME, 'ivu-icon-ios-calendar-outline')))  
            rows = [5, 5, 2]
            return rows
        except:
            if retry < 2:
                self.select_qdb(retry + 1)
        


    def select_54(self, retry = 0):
        print('Selecting 54...')
        try:
            WebDriverWait(self.driver, 3).until(EC.visibility_of(self.driver.find_element(By.CLASS_NAME, 'homeWrap')))
            self.driver.find_element(By.CLASS_NAME, 'homeWrap').\
                find_element(By.CLASS_NAME, 'header').\
                    find_element(By.CLASS_NAME, 'headerContent').\
                        find_elements(By.CLASS_NAME, 'tabItem')[1].click()
            WebDriverWait(self.driver, 3).until(EC.url_to_be('https://epe.pku.edu.cn/venue/pku/venue-introduce?selectIndex=1'))
            WebDriverWait(self.driver, 3).until(EC.visibility_of(self.driver.find_element(By.CLASS_NAME, 'venueList')))
            # venueItem:qdb venueDetailBottomItem:羽毛球场
            self.driver.find_element(By.CLASS_NAME, 'venueList').\
            find_elements(By.CLASS_NAME, 'venueItem')[1].\
                find_element(By.CLASS_NAME, 'venueDetailBottom').\
                    find_elements(By.CLASS_NAME, 'venueDetailBottomItem')[0].click() 
            WebDriverWait(self.driver, 3).until(EC.url_to_be('https://epe.pku.edu.cn/venue/pku/venue-reservation/86'))
            # date
            WebDriverWait(self.driver, 3).until(EC.visibility_of(self.driver.find_element(By.CLASS_NAME, 'ivu-icon-ios-calendar-outline')))        
            rows = [5, 4]
            return rows
        except:
            self.select_54(retry + 1)


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
        self.display_all()
        self.verify()
        WebDriverWait(self.driver, 3).until(lambda _:len(self.driver.find_elements(By.CLASS_NAME, 'cardPay'))>0)
        self.driver.find_elements(By.CLASS_NAME, 'cardPay')[0].click()
        self.driver.find_elements(By.CLASS_NAME, 'ivu-btn')[1].click()
        cnt += 1
        return cnt


    def verify(self):
        print('Verifying...')
        self.save_img()
        distance = img_compute_edge()
        tracks = get_track(distance)
        print (tracks)
        ans = self.slide(tracks)
        print ('滑动结果:' + str(ans))
        if ans == -1:
            time.sleep(0.5)
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
        
        ActionChains(self.driver).click_and_hold(block).perform()
        print('move on')
        for item in tracks:
            ActionChains(self.driver).move_by_offset(xoffset=item, yoffset=random.randint(-1,1)).perform()
        # 稳定一秒再松开
        time.sleep(0.1)
        ActionChains(self.driver).release(block).perform()
        self.driver.get_screenshot_as_file('./pics/verilator.png')
        
        ans_path = '/html/body/div[1]/div/div/div[3]/div[2]/div/div[2]/div[2]/div/div[2]/div/div[1]/div'
        ans = self.driver.find_element_by_xpath(ans_path)

        if '验证成功' in ans.text:
            return 1
        return -1


    def display_all(self):
        js_display_mask = 'document.getElementsByClassName("mask")[0].style.display="block";'
        self.driver.execute_script(js_display_mask)

        js_remove_style = 'arguments[0].removeAttribute("style");'
        relative = self.driver.find_element_by_xpath('/html/body/div[1]/div/div/div[3]/div[2]/div/div[2]/div[2]/div/div[2]/div')
        self.driver.execute_script(js_remove_style, relative)


def wechat_notification(boot_info, sckey):
    with request.urlopen(
            quote('https://sctapi.ftqq.com/' + sckey + '.send?title=场地预约成功&desp=' +
                        boot_info + '\n',
                        safe='/:?=&')) as response:
        response = json.loads(response.read().decode('utf-8'))
        print(response)


