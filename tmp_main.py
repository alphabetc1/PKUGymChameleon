from action import *

if __name__ == '__main__':
    
    #TODO 配置文件与解析
    ID = 'x' # 学号
    PASSWORD = 'x' # 密码
    PHONE_NUMBER = 'x' #电话
    REFRESH_INTERVAL = 0.8 # 抢场地的重试间隔 单位：seconds

    DATE = '2021-12-01'
    TIMES = [19, 20] # [19]表示订19-20， [19, 20]表示定19-21，目前只支持这两种用法。
    SITES = [3, 4, 9, 10, 2, 5, 8, 11, 1, 6, 7, 12] # 按照这个顺序尝试订场
    
    try:
        # initialize
        driver = Chrome()
        sorted(TIMES)

        login(driver, ID, PASSWORD)

        # TODO 可配置体育馆、项目
        # 用枚举变量或map存储体育馆和项目的index
        # reserve的逻辑也需要跟着改
        selectGymAndSport(driver, DATE)

        retry = True
        reserve(driver, DATE, TIMES, SITES, PHONE_NUMBER, REFRESH_INTERVAL, retry)
        
    except Exception as e:
        print(e)
        driver.quit()

    driver.quit()
