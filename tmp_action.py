from selenium.webdriver import Chrome
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.common.by import By

def login(driver, ID, PASSWORD):
    try:
        driver.maximize_window()
        driver.get("https://epe.pku.edu.cn/venue/pku/Login")
        WebDriverWait(driver, 3).until(EC.visibility_of(driver.find_element(By.CLASS_NAME, 'loginFlagWrapItem')))
        loginButton = driver.find_element(By.CLASS_NAME, 'loginFlagWrapItem')
        loginButton.click()
        # portal login
        WebDriverWait(driver, 3).until(EC.url_to_be('https://iaaa.pku.edu.cn/iaaa/oauth.jsp'))
        WebDriverWait(driver, 3).until(EC.visibility_of(driver.find_element(By.ID, 'user_name')))
        IDBlock = driver.find_element(By.ID, 'user_name')
        passwordBlock = driver.find_element(By.ID, 'password')
        IDBlock.send_keys(ID)
        passwordBlock.send_keys(PASSWORD)
        loginButton = driver.find_element(By.ID, 'logon_button')
        loginButton.click()
        WebDriverWait(driver, 3).until(EC.url_to_be('https://epe.pku.edu.cn/venue/PKU/home'))
    except:
        pass

def selectGymAndSport(driver, DATE):
    driver.find_element(By.CLASS_NAME, 'tabWrap').\
        find_elements(By.CLASS_NAME, 'tabItem')[1].click()
    WebDriverWait(driver, 3).until(EC.url_to_be('https://epe.pku.edu.cn/venue/pku/venue-introduce?selectIndex=1'))
    WebDriverWait(driver, 3).until(EC.visibility_of(driver.find_element(By.CLASS_NAME, 'venueList')))
    driver.find_element(By.CLASS_NAME, 'venueList').\
        find_elements(By.CLASS_NAME, 'venueItem')[0].\
            find_element(By.CLASS_NAME, 'venueDetailBottom').\
                find_elements(By.CLASS_NAME, 'venueDetailBottomItem')[0].click()

    WebDriverWait(driver, 3).until(EC.url_to_be('https://epe.pku.edu.cn/venue/pku/venue-reservation/60'))
    WebDriverWait(driver, 3).until(EC.visibility_of(driver.find_element(By.CLASS_NAME, 'ivu-icon-ios-calendar-outline')))
    driver.find_element(By.CLASS_NAME, 'ivu-icon-ios-calendar-outline').click()
    driver.find_element(By.CLASS_NAME, 'ivu-input-with-suffix').send_keys(DATE)
    driver.find_element(By.CLASS_NAME, 'ivu-icon-md-refresh').click()
    # driver.find_element(By.CLASS_NAME, 'ivu-input-with-suffix').clear()

def setDate(driver, date, REFRESH_INTERVAL):
    driver.find_element(By.CLASS_NAME, 'ivu-icon-ios-calendar-outline').click()
    driver.find_element(By.CLASS_NAME, 'ivu-input-with-suffix').send_keys(date)
    driver.find_element(By.CLASS_NAME, 'ivu-icon-md-refresh').click()
    while True:
        try:
            WebDriverWait(driver, REFRESH_INTERVAL).until(lambda _: len(driver.find_elements(By.CLASS_NAME, 'reserveBlock'))>=30)
            break
        except:
            driver.back()
            driver.forward()
            print('选择日期重试中...')
            WebDriverWait(driver, 3).until(EC.url_to_be('https://epe.pku.edu.cn/venue/pku/venue-reservation/60'))
            WebDriverWait(driver, 3).until(EC.visibility_of(driver.find_element(By.CLASS_NAME, 'ivu-icon-ios-calendar-outline')))
            driver.find_element(By.CLASS_NAME, 'ivu-icon-ios-calendar-outline').click()
            driver.find_element(By.CLASS_NAME, 'ivu-input-with-suffix').send_keys(date)
            driver.find_element(By.CLASS_NAME, 'ivu-icon-md-refresh').click()
    # WebDriverWait(driver, 3).until(EC.visibility_of(driver.find_element(By.CLASS_NAME, 'ivu-icon-md-refresh')))

def reserve(driver, date, times, sitesPriority, PHONE_NUMBER, REFRESH_INTERVAL, retry):
    setDate(driver, date, REFRESH_INTERVAL)
    if len(times)==1:
        reserveSingle(driver, date, times[0], sitesPriority, PHONE_NUMBER)
    elif times[0]+1 == times[1]: 
        reservePair(driver, date, times, sitesPriority, PHONE_NUMBER)
    else:
        raise '只能定一对儿连续的场地'

def reserveSingle(driver, date, time, sitesPriority, PHONE_NUMBER):
    print('-------------------------')
    print('正在预约%s, %d-%d点的场地...'%(date, time, time+1))
    success = False
    for site in sitesPriority:
        driver.find_element(By.CLASS_NAME, 'ivu-icon-md-refresh').click()
        print('尝试订%d号场...'%site)
        page = (site-1)//5
        for i in range(page):
            WebDriverWait(driver, 3).until(lambda _:len(driver.find_elements(By.CLASS_NAME, 'pull-right'))>0)
            driver.find_elements(By.CLASS_NAME, 'pull-right')[0].click()
        WebDriverWait(driver, 3).until(lambda _: len(driver.find_elements(By.CLASS_NAME, 'reserveBlock'))>=30)
        reserveBlocks = driver.find_elements(By.CLASS_NAME, 'reserveBlock')
        index = 0
        if site > 10:
            index = (time-8)*2+(site-1)%5
        else:
            index = (time-8)*5+(site-1)%5
        if reserveBlocks[index].get_attribute('class').find('free') != -1:
            reserveBlocks[index].click()
            driver.find_element(By.CLASS_NAME, 'ivu-checkbox-input').click()
            driver.find_elements(By.CLASS_NAME, 'payHandleItem')[1].click()
            WebDriverWait(driver, 3).until(lambda _:len(driver.find_elements(By.CLASS_NAME, 'ivu-input-default'))==5)
            driver.find_elements(By.CLASS_NAME, 'ivu-input-default')[0].\
                    clear()
            driver.find_elements(By.CLASS_NAME, 'ivu-input-default')[0].\
                    send_keys(PHONE_NUMBER)
            driver.find_elements(By.CLASS_NAME, 'payHandleItem')[1].click()
            WebDriverWait(driver, 3).until(lambda _:len(driver.find_elements(By.CLASS_NAME, 'cardPay'))>0)
            driver.find_elements(By.CLASS_NAME, 'cardPay')[0].click()
            driver.find_elements(By.CLASS_NAME, 'ivu-btn')[1].click()
            print('成功订到%s, %d-%d点的%d号场' %(date, time, time+1, site))
            success = True
            break
        else:
            print('%d号场不行'%site)

        # driver.find_element(By.CLASS_NAME, 'payHandleItem').click()
        # WebDriverWait(driver, 300).until(lambda driver:False)
    if not success:
        print('%s:%d-%d的场地预定失败'%(date, time, time+1))

def reservePair(driver, date, times, sitesPriority, PHONE_NUMBER):
    print('-------------------------')
    print('正在预约%s, %d-%d点的场地...'%(date, times[0], times[0]+2))
    success = False
    for site in sitesPriority:
        driver.find_element(By.CLASS_NAME, 'ivu-icon-md-refresh').click()
        print('尝试订%d号场...'%site)
        page = (site-1)//5
        for i in range(page):
            WebDriverWait(driver, 3).until(lambda _:len(driver.find_elements(By.CLASS_NAME, 'pull-right'))>0)
            driver.find_elements(By.CLASS_NAME, 'pull-right')[0].click()
        WebDriverWait(driver, 3).until(lambda _: len(driver.find_elements(By.CLASS_NAME, 'reserveBlock'))>=30)
        reserveBlocks = driver.find_elements(By.CLASS_NAME, 'reserveBlock')
        index1 = index2 = 0
        if site > 10:
            index1 = (times[0]-8)*2+(site-1)%5
            index2 = (times[1]-8)*2+(site-1)%5
        else:
            index1 = (times[0]-8)*5+(site-1)%5
            index2 = (times[1]-8)*2+(site-1)%5
        if reserveBlocks[index1].get_attribute('class').find('free') != -1 and reserveBlocks[index2].get_attribute('class').find('free') != -1:
            reserveBlocks[index1].click()
            reserveBlocks[index2].click()
            driver.find_element(By.CLASS_NAME, 'ivu-checkbox-input').click()
            driver.find_elements(By.CLASS_NAME, 'payHandleItem')[1].click()
            WebDriverWait(driver, 30).until(lambda _:len(driver.find_elements(By.CLASS_NAME, 'ivu-input-default'))==5)
            driver.find_elements(By.CLASS_NAME, 'ivu-input-default')[0].\
                    clear()
            driver.find_elements(By.CLASS_NAME, 'ivu-input-default')[0].\
                    send_keys(PHONE_NUMBER)
            driver.find_elements(By.CLASS_NAME, 'payHandleItem')[1].click()
            WebDriverWait(driver, 30).until(lambda _:len(driver.find_elements(By.CLASS_NAME, 'cardPay'))>0)
            driver.find_elements(By.CLASS_NAME, 'cardPay')[0].click()
            driver.find_elements(By.CLASS_NAME, 'ivu-btn')[1].click()
            print('成功订到%s, %d-%d点的%d号场' %(date, times[0], times[0]+2, site))
            success = True
            break
        else:
            print('%d号场不行'%site)

        # driver.find_element(By.CLASS_NAME, 'payHandleItem').click()
        # WebDriverWait(driver, 300).until(lambda driver:False)
    if not success:
        print('%s:%d-%d的场地预定失败'%(date, times[0], times[0]+2))
