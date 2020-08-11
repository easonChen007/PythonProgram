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

class TheNorthFace():
    """
    北面商品监控
    """
    session = None
    path = None

    def __init__(self):
        self.session = Request()
        sys_str = platform.system()

        # 驱动路径        
        if sys_str == "Windows":
            path = Config().CHROME_DRIVER_WIN_PATH
        elif sys_str == "Linux":
            path = Config().CHROME_DRIVER_MAC_PATH
        else:
            path = Config().CHROME_DRIVER_MAC_PATH

    @classmethod
    def start(cls, content=''):
        self = cls()
        self.start_monitor()
        stay_second(600, self.start)

    def start_monitor(self, content=None):
        for v_tnf_addr in Config().TNF_WEB_ADDR:
            product_name = v_tnf_addr.get('product_name')
            addr = v_tnf_addr.get('addr')
            print(product_name)
            #print( addr )
            create_thread_and_run(self, 'run_event', False,
                                  args=(product_name, addr,))

    def run_event(self, product_name, addr):
        # 打开浏览器
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')

        # 创建浏览器对象
        driver = webdriver.Chrome(
            executable_path=path, chrome_options=chrome_options)
        # driver.get('https://www.thenorthface.com/shop/1990-mountain-jacket-gtx-nf0a3xco-c1?variationId=9B8#hero=0')
        if addr:
            try:
                driver.get(addr)
            except Exception as e:
                # 连接超时
                CommonLog.add_quick_log('连接超时').flush()
                return

            time.sleep(20)
            # 遍历商品颜色 依次点击获取型号库存状态
            element = driver.find_elements_by_xpath(
                '//*[@id="product-attr-form"]/section[1]/div[2]/div/button')
            for e_product_color in element:
                #driver.execute_script("arguements[0].click();", e_product_color)
                try:
                    e_product_color.click()
                except Exception as e:
                    pass

                time.sleep(1)
                # 商品颜色状态
                v_product_color_status = e_product_color.get_attribute('class')
                if v_product_color_status.find('out-of-stock') >= 0:
                    v_product_color_status = 'out-of-stock'
                else:
                    v_product_color_status = 'in-stock'
                v_product_color_name = e_product_color.get_attribute(
                    'data-attribute-value')

                s_main_product_color = '货名={0} 颜色={1} 库存状态={2}'.format(
                    product_name, v_product_color_name, v_product_color_status)
                # CommonLog.add_quick_log('货名={0} 颜色={1} 库存状态={2}'.format(
                #    product_name, v_product_color_name, v_product_color_status)).flush()

                # 对应颜色型号库存状态
                element_model = driver.find_elements_by_xpath(
                    '//*[@id="product-attr-form"]/section[2]/div[2]/div/button')

                s_sub_product_model = ''
                for e_product_model in element_model:
                    v_product_model_name = e_product_model.get_attribute(
                        'data-attribute-value')
                    v_product_model_status = e_product_model.get_attribute(
                        'class')
                    if v_product_model_status.find('out-of-stock') >= 0:
                        v_product_model_status = '无'
                    else:
                        v_product_model_status = '有'

                    s_sub_product_model += 'SIZE={0} 库存状态={1},'.format(
                        v_product_model_name, v_product_model_status)

                CommonLog.add_quick_log(
                    s_main_product_color+' 【'+s_sub_product_model + '】').flush()

                Notification.send_to_telegram(
                    s_main_product_color+' 【'+s_sub_product_model + '】')

                print('end')


if __name__ == '__main__':
    pass
