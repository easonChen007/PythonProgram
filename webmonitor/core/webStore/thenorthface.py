import urllib

from core.config import Config
from core.helpers.api import *
from core.helpers.request import Request
from core.log.common_log import CommonLog

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options


class TheNorthFace():
    """
    北面商品监控
    """
    session = None

    def __init__(self):
        self.session = Request()

    @classmethod
    def start(cls, content=''):
        self = cls()
        self.start_monitor(content=content)

   
    def start_monitor(self, content):
        #打开浏览器
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        # 驱动路径
        path = Config().CHROME_DRIVER_MAC_PATH
        # 创建浏览器对象
        driver = webdriver.Chrome(executable_path=path, chrome_options=chrome_options)
        driver.get('https://www.thenorthface.com/shop/1990-mountain-jacket-gtx-nf0a3xco-c1?variationId=9B8#hero=0')

        time.sleep(10)
        element = driver.find_elements_by_xpath('//*[@id="product-attr-form"]/section[1]/div[2]/div/button')
        for post_title in element:
            print( post_title.get_attribute('class'))
            print( 'end')


if __name__ == '__main__':
    pass
