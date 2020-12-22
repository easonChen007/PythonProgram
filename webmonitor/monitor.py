import requests
import time
import lxml.html
import sys

from core.app import *
from core.log.common_log import CommonLog
#from core.webStore.thenorthface import TheNorthFace
from core.webStore.stock_trace import Stock_Trace
from core.webStore.gshock import CASIO_GSHOCK
from core.webStore.madness import SEEK_MADNESS
#from core.db.oracle_control import Oracle_Control

'''
source = requests.get('https://www.thenorthface.com/shop/1990-mountain-jacket-gtx-nf0a3xco-c1?variationId=9B8#hero=0').content

selector = lxml.html.fromstring(source)
post_title_list = selector.xpath('//*[@id="product-attr-form"]/section[1]/div[2]/div/button/@class')
for post_title in post_title_list:
    print(  post_title)
'''

def main():
    #App.test_send_notifications()
    App.run()
    #tnf = TheNorthFace()
    #tnf.start()

    #st = Stock_Trace()
    #st.start()

    ca = SEEK_MADNESS()
    ca.start()



if __name__ == '__main__':
    main()
    

while True:
 pass



