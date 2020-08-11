# -*- coding: utf-8 -*-

# 查询间隔(指每一个任务中每一个日期的间隔 / 单位秒)
# 默认取间隔/2 到 间隔之间的随机数 如设置为 1 间隔则为 0.5 ~ 1 之间的随机数
# 接受字典形式 格式:    {'min': 0.5, 'max': 1}
QUERY_INTERVAL = 1

# 用户心跳检测间隔 格式同上
USER_HEARTBEAT_INTERVAL = 120

# 多线程查询
QUERY_JOB_THREAD_ENABLED = 0  # 是否开启多线程查询，开启后第个任务会单独分配线程处理

# 打码平台账号
# 目前只支持免费打码接口 和 若快打码，注册地址：http://www.ruokuai.com/login
# 免费填写 free 若快 ruokuai  # 免费打码无法保证持续可用，如失效请手动切换; 个人打码填写 user 并修改API_USER_CODE_QCR_API 为自己地址
AUTO_CODE_PLATFORM = 'free'
API_USER_CODE_QCR_API = ''
AUTO_CODE_ACCOUNT = {  # 使用 free 可用省略
    'user': 'your user name',
    'pwd': 'your password'
}

# 语音验证码
# 没找到比较好用的，现在用的这个是阿里云 API 市场上的，基本满足要求，价格也便宜
# 购买成功后到控制台找到  APPCODE 放在下面就可以了
# 地址：易源 https://market.aliyun.com/products/57126001/cmapi019902.html
# 2019-01-18 更新
# 增加新的服务商 鼎信 https://market.aliyun.com/products/56928004/cmapi026600.html?spm=5176.2020520132.101.2.e27e7218KQttQS
NOTIFICATION_BY_VOICE_CODE = 0  # 开启语音通知
NOTIFICATION_VOICE_CODE_TYPE = 'dingxin'  # 语音验证码服务商  可用项 dingxin  yiyuan
NOTIFICATION_API_APP_CODE = 'your app code'
NOTIFICATION_VOICE_CODE_PHONE = 'your phone'  # 接受通知的手机号

# 钉钉通知
# 使用说明   https://open-doc.dingtalk.com/docs/doc.htm?treeId=257&articleId=105735&docType=1
DINGTALK_ENABLED = 0
DINGTALK_WEBHOOK = 'https://oapi.dingtalk.com/robot/send?access_token=your token'

# Telegram消息推送
# 目前共有两个Bot：
#   1：https://t.me/notificationme_bot
#   2：https://t.me/RE_Link_Push_bot
# 任选一个Bot，关注获取URL链接，如果没有回复则发送给Bot这条信息: /start
# 将获取的URL填入下面对应位置
# 注意：因为以上Bot都由他人公益提供，无法保证随时可用，如以上Bot都无法使用，请使用其他消息推送方式
# Bot1来源：https://github.com/Fndroid/tg_push_bot
# Bot2来源：https://szc.me/post/2.html
TELEGRAM_ENABLED = 1
TELEGRAM_BOT_API_URL = 'https://tgbot.lbyczf.com/sendMessage/9qvmsoktk7oy2kwl'


# ServerChan 和 PushBear 微信消息推送
# 使用说明
# ServerChan     http://sc.ftqq.com
# PushBear       http://pushbear.ftqq.com
SERVERCHAN_ENABLED = 0
SERVERCHAN_KEY = ''
PUSHBEAR_ENABLED = 0
PUSHBEAR_KEY = '19635-0f2efc0e9911cf5da47cb66ce43c2ba5'

# Bark 推送到ios设备
# 参考 https://www.v2ex.com/t/467407
BARK_ENABLED = 1
BARK_PUSH_URL = 'https://api.day.app/dobqmRBaKPMiyFXkE4Wzf8/'

# 输出日志到文件
OUT_PUT_LOG_TO_FILE_ENABLED = 1
OUT_PUT_LOG_TO_FILE_PATH = 'c:/runtime/monitor.log'  # 日志目录

# 分布式集群配置
CLUSTER_ENABLED = 0  # 集群状态
NODE_IS_MASTER = 1  # 是否是主节点 同时只能启用 1 个主节点
NODE_SLAVE_CAN_BE_MASTER = 1  # 主节点宕机后，子节点是否可以自动提升为主节点(建议打开)
NODE_NAME = 'master'  # 节点名称，不能重复
REDIS_HOST = 'localhost'  # Redis  host
REDIS_PORT = '6379'  # Redis  port
REDIS_PASSWORD = ''  # Redis  密码 没有可以留空

# 邮箱配置
EMAIL_ENABLED = 0  # 是否开启邮件通知
EMAIL_SENDER = 'sender@example.com'  # 邮件发送者
# 邮件接受者 # 可以多个 [email1@gmail.com, email2@gmail.com]
EMAIL_RECEIVER = 'receiver@example.com'
EMAIL_SERVER_HOST = 'localhost'  # 邮件服务 host
EMAIL_SERVER_USER = ''  # 邮件服务登录用户名
EMAIL_SERVER_PASSWORD = ''  # 邮件服务登录密码

# Web 管理
WEB_ENABLE = 1  # 是否打开 Web 管理
WEB_USER = {  # 登录信息
    'username': 'admin',
    'password': 'password'
}
WEB_PORT = 8008  # 监听端口

# 是否开启 CDN 查询
CDN_ENABLED = 0
CDN_CHECK_TIME_OUT = 1  # 检测单个 cdn 是否可用超时时间

# 是否使用浏览器缓存中的RAIL_EXPIRATION 和 RAIL_DEVICEID
CACHE_RAIL_ID_ENABLED = 0
RAIL_EXPIRATION = ''  # 浏览12306 网站中的Cache的RAIL_EXPIRATION 值
RAIL_DEVICEID = ''  # 浏览12306 网站中的Cache的RAIL_DEVICEID 值

TEST_V = 2
TEST_V2 = 1

# chrome diver 路径
CHROME_DRIVER_MAC_PATH = 'E:\chromedriver_win32\chromedriver.exe'
CHROME_DRIVER_WIN_PATH = 'E:\chromedriver_win32\chromedriver.exe'

# the north face monitor address
TNF_WEB_ADDR = [
    {'product_name': '1990-mountain-jacket-gtx',
     'addr': 'https://www.thenorthface.com/shop/1990-mountain-jacket-gtx-nf0a3xco-c1?variationId=9B8#hero=0'},
    {'product_name': 'mens-apex-risor-jacket',
     'addr': ''}
]

# the north face monitor address
CASIO_WEB_ADDR = [
    {'product_name': 'GA-2100-1A1PR',
     'addr': 'https://m.casiostore.com.cn/watch/g-shock/GA-2100/s5200.html'}
]
