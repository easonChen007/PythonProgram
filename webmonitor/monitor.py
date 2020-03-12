import requests
import time
import lxml.html
import sys

from core.app import *
from core.log.common_log import CommonLog

'''
source = requests.get('https://www.thenorthface.com/shop/1990-mountain-jacket-gtx-nf0a3xco-c1?variationId=9B8#hero=0').content

selector = lxml.html.fromstring(source)
post_title_list = selector.xpath('//*[@id="product-attr-form"]/section[1]/div[2]/div/button/@class')
for post_title in post_title_list:
    print(  post_title)
'''

def main():
    App.test_send_notifications()
    App.run()

if __name__ == '__main__':
    main()
    

while True:
 pass

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

#打开浏览器
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
# 驱动路径
path = 'E:\chromedriver_win32\chromedriver.exe'
# 创建浏览器对象
driver = webdriver.Chrome(executable_path=path, chrome_options=chrome_options)

driver.get('https://www.thenorthface.com/shop/1990-mountain-jacket-gtx-nf0a3xco-c1?variationId=9B8#hero=0')

#time.sleep(10)

element = driver.find_elements_by_xpath('//*[@id="product-attr-form"]/section[1]/div[2]/div/button')
for post_title in element:
   print( post_title.get_attribute('class'))
print( 'end')