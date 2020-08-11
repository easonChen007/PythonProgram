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


class CASIO_GSHOCK():
    """
    gshock监控
    """
    session = None
    path = None

    def __init__(self):
        self.session = Request()
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
        self.start_monitor()

    def start_monitor(self, content=None):
        while True:
            for v_casio_addr in Config().CASIO_WEB_ADDR:
                product_name = v_casio_addr.get('product_name')
                addr = v_casio_addr.get('addr')
                print(product_name)
                #print( addr )
                create_thread_and_run(self, 'run_event', False,
                                      args=(product_name, addr,))
            stay_second(900)

    def run_event(self, product_name, addr):
        # 打开浏览器
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')

        # 创建浏览器对象
        driver = webdriver.Chrome(
            executable_path=self.path, chrome_options=chrome_options)
        # driver.get('https://www.thenorthface.com/shop/1990-mountain-jacket-gtx-nf0a3xco-c1?variationId=9B8#hero=0')
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
                '//*[@id="J_product_buyOperate"]/div/button')

            for e_product_color in element:
                #driver.execute_script("arguements[0].click();", e_product_color)
                # try:
                #    e_product_color.click()
                # except Exception as e:
                #    pass

                CommonLog.add_quick_log(e_product_color.text).flush()
                Notification.push_bark(e_product_color.text)
                #Notification.push_bear(e_product_color.text)
                print(e_product_color.text)


if __name__ == '__main__':
    pass
