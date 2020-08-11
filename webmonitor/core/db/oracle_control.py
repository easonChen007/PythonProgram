import urllib
import cx_Oracle

from core.config import Config
from core.helpers.api import *
from core.helpers.request import Request
from core.log.common_log import CommonLog
from core.helpers.func import *
from core.helpers.notification import Notification

import platform


class Oracle_Control():
    """
    orcale 数据库管理
    """
    session = None
    or_client_path = None
    s_result = None
    connectObj = ""
    connCnt = 0
    cursorCnt = 0

    oracle_pool = None
    connCnt_pool = 0

    def __init__(self):
        self.session = Request()
        sys_str = platform.system()

        # 驱动路径
        if sys_str == "Windows":
            self.or_client_path = Config().ORACLE_CLIENT_WIN_PATH
        elif sys_str == "Linux":
            self.or_client_path = Config().ORACLE_CLIENT_WIN_PATH
        else:
            self.or_client_path = Config().ORACLE_CLIENT_WIN_PATH

        #  notice python 64位 instantclient-basic 64位 cx_oracle 64位
        cx_Oracle.init_oracle_client(lib_dir=self.or_client_path)

    def initOracleConnect(self, content=''):
        if self.connCnt == 0:
            self.connectObj = cx_Oracle.connect(
                Config().ORACLE_SERVER_PATH)  # 用自己的实际数据库用户名、密码、主机ip地址 替换即可
            self.connCnt += 1

    def getOracleConnect(self):
         self.initOracleConnect()
         return self.connectObj

    def closeOracleConnect(self, connectObj):
        connectObj.close()
        self.connCnt -= 1

    def getOracleCursor(self):
        self.initOracleConnect()
        self.cursorCnt += 1
        return self.connectObj.cursor()

    def closeOracleCursor(self, cursorObj):
        cursorObj.close()
        self.cursorCnt -= 1
        if self.cursorCnt == 0:
            print("will close conn")
            self.closeOracleConnect(self.connectObj)

    def selectFromDbTable(self, sql, argsDict):
        # 将查询结果由tuple转为list
        queryAnsList = []
        selectCursor = self.getOracleCursor()
        selectCursor.prepare(sql)
        queryAns = selectCursor.execute(None, argsDict)
        for ansItem in queryAns:
            queryAnsList.append(list(ansItem))

        self.closeOracleCursor(selectCursor)
        return queryAnsList
        
    def getOracleConnect_withPool(self):
        if self.oracle_pool is None:
            # 创建连接池
            self.oracle_pool = cx_Oracle.SessionPool(Config().ORACLE_SERVER_USERNAME, Config().ORACLE_SERVER_SECRET,
                                                     Config().ORACLE_SERVER_CONNECTSTRING, min=2, max=10, increment=1, threaded=True, encoding="UTF-8")
            # print(self.oracle_pool.max_lifetime_session)
        t_connectObj_pool = self.oracle_pool.acquire()
        self.connCnt_pool += 1
        return t_connectObj_pool
    

    def closeOracleConnect_withPool(self, connectObj_pool):
        if self.oracle_pool is not None:
            self.oracle_pool.release(connectObj_pool)
        self.connCnt_pool -= 1

    def releasePool(self):
        if self.connCnt_pool == 0 and self.oracle_pool is not None:
            self.oracle_pool.close()
            self.oracle_pool = None




"""
    def closeConn(self, content=None):
        curs=conn.cursor()
        sql='select * from ucap_user' #sql语句
        rr=curs.execute (sql)
        row=curs.fetchone()
        print(row)
        curs.close()
        conn.close()
        
"""

if __name__ == '__main__':
    pass
