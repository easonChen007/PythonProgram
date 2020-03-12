# -*- coding: utf-8 -*-
import os
import signal
import sys

from core.helpers.func import *
from core.config import Config
from core.helpers.notification import Notification
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

    @classmethod
    def test_send_notifications(cls):
        if Config().NOTIFICATION_BY_VOICE_CODE:  # 语音通知
            CommonLog.add_quick_log(CommonLog.MESSAGE_TEST_SEND_VOICE_CODE).flush()
            if Config().NOTIFICATION_VOICE_CODE_TYPE == 'dingxin':
                voice_content = {'left_station': '广州', 'arrive_station': '深圳', 'set_type': '硬座', 'orderno': 'E123542'}
            else:
                pass
                #voice_content = OrderLog.MESSAGE_ORDER_SUCCESS_NOTIFICATION_OF_VOICE_CODE_CONTENT.format('北京','深圳')
                
            Notification.voice_code(Config().NOTIFICATION_VOICE_CODE_PHONE, '张三', voice_content)
        if Config().EMAIL_ENABLED:  # 邮件通知
            CommonLog.add_quick_log(CommonLog.MESSAGE_TEST_SEND_EMAIL).flush()
            Notification.send_email(Config().EMAIL_RECEIVER, '测试发送邮件', 'By py12306')

        if Config().DINGTALK_ENABLED:  # 钉钉通知
            CommonLog.add_quick_log(CommonLog.MESSAGE_TEST_SEND_DINGTALK).flush()
            Notification.dingtalk_webhook('测试发送信息')

        if Config().TELEGRAM_ENABLED:  # Telegram通知
            CommonLog.add_quick_log(CommonLog.MESSAGE_TEST_SEND_TELEGRAM).flush()
            Notification.send_to_telegram('测试发送信息')

        if Config().SERVERCHAN_ENABLED:  # ServerChan通知
            CommonLog.add_quick_log(CommonLog.MESSAGE_TEST_SEND_SERVER_CHAN).flush()
            Notification.server_chan(Config().SERVERCHAN_KEY, '测试发送消息', 'By py12306')

        if Config().PUSHBEAR_ENABLED:  # PushBear通知
            CommonLog.add_quick_log(CommonLog.MESSAGE_TEST_SEND_PUSH_BEAR).flush()
            Notification.push_bear(Config().PUSHBEAR_KEY, '测试发送消息', 'By py12306')

        if Config().BARK_ENABLED:  # Bark通知
            CommonLog.add_quick_log(CommonLog.MESSAGE_TEST_SEND_PUSH_BARK).flush()
            Notification.push_bark('测试发送信息')

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
