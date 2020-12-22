import urllib

from core.config import Config
from core.helpers.api import *
from core.helpers.request import Request
from core.log.common_log import CommonLog
from core.helpers.func import *
from core.helpers.notification import Notification

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import platform

import requests
import requests.utils
import pickle
from requests.exceptions import *
from lxml.html import fromstring

requests.packages.urllib3.disable_warnings()

class SEEK_MADNESS():
    """
    madness监控 /html/body/div[1]/div[4]/div/div[3]/div[1]/div[1]/select/option[3]
    """
    session = None
    path = None

    def __init__(self, usr_name=None, usr_pwd=None):
        # cookie info
        self.trackid = ''
        self.uuid = ''
        self.eid = ''
        self.fp = ''

        self.usr_name = '1544934946@qq.com'
        self.usr_pwd = '2233234'
        self.interval = 0

        # init url related
        self.home = 'https://passport.jd.com/new/login.aspx'

        self.sess = requests.Session()

        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36',
            'ContentType': 'text/html; charset=utf-8',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Connection': 'keep-alive',
        }

        self.cookies = {

        }

        #self.session = Request() #原封装类
        sys_str = platform.system()

        # 驱动路径
        if sys_str == "Windows":
            self.path = Config().CHROME_DRIVER_WIN_PATH
        elif sys_str == "Linux":
            self.path = Config().CHROME_DRIVER_MAC_PATH
        else:
            self.path = Config().CHROME_DRIVER_MAC_PATH

    @classmethod
    def start(cls, content=''):
        self = cls()

        if self.checkLogin() :
            self.start_monitor()
        else: #再登录一次
            if self.login_start():
                if self.checkLogin() :
                    self.start_monitor()

        # self.checkLogin()
        # self.start_monitor()

    
    def login_start(self):
        response, session ,loginResult= self.login_test()

        if loginResult :
            with open('cookie', 'w') as f:
                #保存方案一 但是非utf-8
                #pickle.dump(session.cookies, f)
                #保存方案二 尝试 json方案             
                json.dump(requests.utils.dict_from_cookiejar(session.cookies), f)
        
            return True
        else:
             print(u'登录失败！')
        return False

    # 表单输入框 查找
    def parse_form(self, html):
        tree = fromstring(html) 
        print(tree)
        data = {}
        for e in tree.cssselect('form input'):
            if e.get('name'):
                data[e.get('name')] = e.get('value')
        return data

    # try login
    def login_test(self, session=None):
        """ Login to example website.
            params:
               session: request lib session object or None
            returns tuple(response, session)
        """
        requests.utils.add_dict_to_cookiejar(self.sess.cookies, self.cookies) 
        #print(self.sess.cookies.get_dict())

        session=self.sess
        response=None

        LOGIN_URL = 'https://www.mdnsonline.com/customer/login'
        if session is None:
            html = requests.get(LOGIN_URL)
        else:
            html = session.get(LOGIN_URL)

        data = self.parse_form(html.content)
        data['CustomerLoginForm[email]'] = self.usr_name
        data['CustomerLoginForm[password]'] = self.usr_pwd
        if session is None:
            response = requests.post(LOGIN_URL, data, cookies=html.cookies, headers =self.headers)
            # response = requests.post(LOGIN_URL, data, cookies=html.cookies, headers =self.headers ,allow_redirects=False)
        else:
            response = session.post(LOGIN_URL, data, headers =self.headers)

        if response.url.find('login') >= 0:
            loginResult = False
        else:
            loginResult = True

        response.encoding='utf-8'
        #print(session.cookies.get_dict() )
        #print(response.cookies.get_dict() )
            
        return response, session ,loginResult
        

    # 检查是否登录
    def checkLogin(self):
        checkUrl = 'https://www.mdnsonline.com/customer/login'

        try:
            print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++')
            print(u'{0} > 自动登录中... '.format(time.ctime()))
            with open('cookie', 'r') as f:
                #cookies = requests.utils.cookiejar_from_dict(pickle.load(f))
                session = self.sess
                session.cookies.update(requests.utils.cookiejar_from_dict(json.load(f)))
                response = session.get(checkUrl)

                if response.url.find('login') >= 0:
                    loginResult = False
                else:
                    loginResult = True

                if loginResult:
                    return True
                else:
                    print(u'登录过期， 请重新登录！')
                    return False
                   
            return False
        except Exception as e:
            return False
        else:
            pass
        finally:
            pass

        return False


    def start_monitor(self, content=None):
        while True:
            for v_madness_addr in Config().MADNESS_WEB_ADDR:
                product_name = v_madness_addr.get('product_name')
                addr = v_madness_addr.get('addr')
                print(product_name)
                #print( addr )
                create_thread_and_run(self, 'run_event', False,
                                      args=(product_name, addr,))
            stay_second(90000)

    def run_event(self, product_name, addr):
        # 打开浏览器
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')

        # 创建浏览器对象
        driver = webdriver.Chrome(
            executable_path=self.path, chrome_options=chrome_options)
        # driver.get('https://www.thenorthface.com/shop/1990-mountain-jacket-gtx-nf0a3xco-c1?variationId=9B8#hero=0')

        driver.get(addr)
        driver_cookies = driver.get_cookies()

        cookiesList = []

        with open('cookie', 'r') as f:
                cookies = json.load(f)
                     # for cookie in cookies:
                     # cookie.pop('domain')  # 如果报domain无效的错误
                for key, value in cookies.items():
                            cookies_t={}
                            cookies_t['name'] = key
                            cookies_t['value'] = value
                            cookiesList.append(cookies_t)
        
        for cookie_a in driver_cookies:
             for cookie_c in cookiesList:
                    if cookie_a['name'] == cookie_c['name']:
                        cookie_a['value'] = cookie_c['value']



        driver.delete_all_cookies()
        for cookie in driver_cookies:
            driver.add_cookie(cookie)

        if addr:
            try:
                driver.get(addr)
            except Exception as e:
                # 连接超时
                CommonLog.add_quick_log('连接超时').flush()
                return

            time.sleep(10)
            # 遍历商品颜色 依次点击获取型号库存状态
            element = driver.find_elements_by_xpath(
                '/html/body/div[1]/div[4]/div/div[3]/p')

            print(element)

            for e_product_color in element:
                #driver.execute_script("arguements[0].click();", e_product_color)
                # try:
                #    e_product_color.click()
                # except Exception as e:
                #    pass

                CommonLog.add_quick_log(e_product_color.text).flush()
                Notification.push_bark(e_product_color.text)
                # Notification.push_bear(e_product_color.text)
                print(e_product_color.text)


if __name__ == '__main__':
    pass
