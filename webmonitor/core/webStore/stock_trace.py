import urllib

from core.config import Config
from core.helpers.api import *
from core.helpers.request import Request
from core.log.common_log import CommonLog
from core.helpers.func import *
from core.helpers.notification import Notification

import platform
import easyquotation
from core.db.oracle_control import *
import json
import uuid


class Stock_Trace():
    """
    股股监控
    """
    session = None
    path = None
    quotation = None
    quotation_timekline = None
    s_result = None
    oc = Oracle_Control()

    def __init__(self):
        self.session = Request()
        sys_str = platform.system()
        # 新浪 ['sina'] 腾讯 ['tencent', 'qq']
        self.quotation = easyquotation.use('sina')
        self.quotation_timekline = easyquotation.use("timekline")

        # 驱动路径
        if sys_str == "Windows":
            path = Config().CHROME_DRIVER_WIN_PATH
        elif sys_str == "Linux":
            path = Config().CHROME_DRIVER_MAC_PATH
        else:
            path = Config().CHROME_DRIVER_MAC_PATH
        # create_thread_and_run(self, 'monitorOracleConNumSer',
        #                      wait=False)

    # 少用递归 python 有递归深度限制，直接用while就可以
    def monitorOracleConNumSer(self):
        create_thread_and_run(self, 'monitorOracleConNum',
                              wait=False)
        stay_second(1, self.monitorOracleConNumSer)  # 六十秒

    def monitorOracleConNum(self):
        print("当前连接数:{}".format(self.oc.connCnt_pool))

    @classmethod
    def start(cls, content=''):
        self = cls()
        self.start_monitor()

    def start_monitor(self, content=None):
        print('stock开始监控')
        while True:
            create_thread_and_run(self, 'run_event', wait=False,
                                  args=('',))
            stay_second(60)

    def run_event(self, arg_a):
        # s_result_dict = self.quotation.real('sh000001')
        # print(s_result_dict)
        print('个股情况')

        str_tmp = ""
        stock_arr = ['sz300498', 'sz000089', 'sz000001', 'sh000001']
        CommonLog.add_quick_log('个股情况 ' + str_tmp.join(stock_arr)).flush()

        # dict 遍历
        data = self.quotation_timekline.real(stock_arr, prefix=True)
        for(k, v) in data.items():

            v_code = k.replace(".js", "")
            v_date = v["date"]
            v_json_time_data = v["time_data"]

            print("分时记录 timekline[%s] [%s]" % (k, v_code))

            oc_conn_pool = self.oc.getOracleConnect_withPool()
            cursor = oc_conn_pool.cursor()
            # 查询分时记录是否存在
            queryAns_c = cursor.execute('select count(1) from EASON_STOCK_RECODE_MIN_DAILY ' +
                                        'WHERE SRMD_DATETIME_DAY = :1 and SRMD_MIN_CODE= :2',
                                        [v_date, v_code])
            resulet_c = queryAns_c.fetchone()[0]

            if resulet_c == 0:
                v_minTime = 0
            else:
                queryAns_c = cursor.execute('select nvl(SRMD_DATETIME,0) from EASON_STOCK_RECODE_MIN_DAILY ' +
                                            'WHERE SRMD_DATETIME_DAY = :1 and SRMD_MIN_CODE= :2 order by SRMD_DATETIME desc ',
                                            [v_date, v_code])
                v_minTime = queryAns_c.fetchone()[0]

            v_minTime = v_minTime if v_minTime else 0

            for v_fs in v_json_time_data:
                v_fs_datetime = v_fs[0]
                if(int(v_fs_datetime) > int(v_minTime)):
                    # 更新成交记录
                    cursor.execute('insert into EASON_STOCK_RECODE_MIN_DAILY (SRMD_MAIN, SRMD_MIN_CODE, SRMD_DATETIME_DAY ,SRMD_DATETIME ,SRMD_NOW_PRICE ,SRMD_NOW_VOLUNM)' +
                                   ' values (:1, :2, :3, :4, :5, :6)',
                                   ["".join(str(uuid.uuid4()).split("-")).upper(), v_code, v_date, v_fs_datetime, v_fs[1], v_fs[2]])
                    oc_conn_pool.commit()

            cursor.close()
            self.oc.closeOracleConnect_withPool(oc_conn_pool)

        resulet_dict = self.quotation.stocks(stock_arr, prefix=True)
        for(k, v) in resulet_dict.items():
            print("dict[%s]=" % k, v)
            # 查询代码是否存在
            sql = ('select count(1) from EASON_STOCK_RECODE_DAILY ' +
                   'WHERE SRD_DATETIME = : P_nowDateTime and SRD_CODE = : P_stockCode')
            oc_conn_pool = self.oc.getOracleConnect_withPool()
            cursor = oc_conn_pool.cursor()
            cursor.prepare(sql)
            queryAns = cursor.execute(
                None, {'P_nowDateTime': v['date'], 'P_stockCode': k})
            v_judge = queryAns.fetchone()[0]  # 是否存在 存在更新 不存在插入
            print(v_judge)  # 是否存在

            if v_judge == 0:
                cursor.execute('insert into EASON_STOCK_RECODE_DAILY (SRD_MAIN, SRD_CODE, SRD_STOCK_NAME, SRD_DATETIME)' +
                               ' values (:1, :2, :3, :4)',
                               ["".join(str(uuid.uuid4()).split("-")).upper(), k, v['name'], v['date']])
                oc_conn_pool.commit()
            else:
                # 更新当前价格
                cursor.execute('update EASON_STOCK_RECODE_DAILY set SRD_DONE_PRICE =:1' +
                               ' where SRD_DATETIME = :2 and SRD_CODE= :3',
                               [v['now'], v['date'], k])
                oc_conn_pool.commit()

                # 更新最高价格
                queryAns_c = cursor.execute('select SRD_MAX_PRICE from EASON_STOCK_RECODE_DAILY ' +
                                            'WHERE SRD_DATETIME = :1 and SRD_CODE= :2',
                                            [v['date'], k])
                resulet_c = 0
                for row in queryAns_c:
                    resulet_c = row[0] if row[0] else 0

                print('查询返回%s' % resulet_c)
                if resulet_c == 0:
                    # 更新最高、低价 Inin
                    cursor.execute('update EASON_STOCK_RECODE_DAILY set SRD_MAX_PRICE =:1,SRD_MIN_PRICE =:2 ' +
                                   ' where SRD_DATETIME = :3 and SRD_CODE= :4',
                                   [v['high'], v['low'], v['date'], k])
                    oc_conn_pool.commit()
                else:
                    queryAns = cursor.execute('select SRD_MAX_PRICE,SRD_MIN_PRICE from EASON_STOCK_RECODE_DAILY ' +
                                              'WHERE SRD_DATETIME = :1 and SRD_CODE= :2',
                                              [v['date'], k])

                    rowResult = queryAns.fetchone()
                    v_maxPrice = rowResult[0] if float(rowResult[0]) else 0
                    v_minPrice = rowResult[1] if float(
                        rowResult[1]) else 100000
                    print("dict[%s]=max:%s min:%s" %
                          (k, v_maxPrice, v_minPrice))

                    if float(v_maxPrice) < float(v['high']):
                        cursor.execute('update EASON_STOCK_RECODE_DAILY set SRD_MAX_PRICE =:1' +
                                       ' where SRD_DATETIME = :2 and SRD_CODE= :3',
                                       [v['high'], v['date'], k])
                        oc_conn_pool.commit()

                    if float(v_minPrice) > float(v['low']):
                        cursor.execute('update EASON_STOCK_RECODE_DAILY set SRD_MIN_PRICE =:1' +
                                       ' where SRD_DATETIME = :2 and SRD_CODE= :3',
                                       [v['low'], v['date'], k])
                        oc_conn_pool.commit()

            cursor.close()
            self.oc.closeOracleConnect_withPool(oc_conn_pool)


'''
        sql = "select count(1) from ucap_user WHERE 1 = :pointId"
        oc_conn_pool = self.oc.getOracleConnect_withPool()

        cursor = oc_conn_pool.cursor()
        cursor.prepare(sql)
        queryAns = cursor.execute(None, {'pointId': '1'})

        queryAnsList = []
        for ansItem in queryAns:
            queryAnsList.append(list(ansItem))
        print(queryAnsList)

        cursor.close()
        self.oc.closeOracleConnect_withPool(oc_conn_pool)
'''

if __name__ == '__main__':
    pass
