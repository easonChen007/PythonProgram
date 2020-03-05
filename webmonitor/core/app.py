# -*- coding: utf-8 -*-
import os
import signal
import sys

from core.helpers.func import *
from core.config import Config
#from core.helpers.notification import Notification
from core.log.common_log import CommonLog

@singleton
class App:
    """
    程序主类
    TODO 代码需要优化
    """

    @classmethod
    def run(cls):
        self = cls()
        #注册退出信号
        self.register_sign()
        self.start()

    def start(self):
        Config().run()
        self.init_class()


    def init_class(self):           
        pass
        return


    def register_sign(self):
        is_windows = os.name == 'nt'
        # if is_windows:
        signs = [signal.SIGINT, signal.SIGTERM]
        # else:
        #     signs = [signal.SIGINT, signal.SIGHUP, signal.SIGTERM] # SIGHUP 会导致终端退出，程序也退出，暂时去掉
        for sign in signs:
            signal.signal(sign, self.handler_exit)

        pass

    def handler_exit(self, *args, **kwargs):
        """
        程序退出
        :param args:
        :param kwargs:
        :return:
        """
        if Config.is_cluster_enabled():
            pass
            #from py12306.cluster.cluster import Cluster
            #Cluster().left_cluster()

        sys.exit()

# Expand
class Dict(dict):
    def get(self, key, default=None, sep='.'):
        keys = key.split(sep)
        for i, key in enumerate(keys):
            try:
                value = self[key]
                if len(keys[i + 1:]) and isinstance(value, Dict):
                    return value.get(sep.join(keys[i + 1:]), default=default, sep=sep)
                return value
            except:
                return self.dict_to_dict(default)

    def __getitem__(self, k):
        return self.dict_to_dict(super().__getitem__(k))

    @staticmethod
    def dict_to_dict(value):
        return Dict(value) if isinstance(value, dict) else value
