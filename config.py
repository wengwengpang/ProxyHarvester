import os

# 版本信息
VERSION = '1.2'

# 数据库设置
DATABASE_PATH = os.path.join(os.path.dirname(__file__), 'proxies.db')

# Web UI设置
SECRET_KEY = os.urandom(24)
DEBUG = False

# 代理源
PROXY_SOURCES = [
    'https://free-proxy-list.net/',
    'https://www.proxynova.com/proxy-server-list/'
]

# 代理检查器设置
TEST_URL = 'http://httpbin.org/ip'
CHECK_INTERVAL = 3600  # 每小时检查一次代理

# 初始用户设置（仅用于开发和测试，生产环境应使用数据库存储）
INITIAL_USER = {
    'username': 'michael',
    'password': 'ab2469843'
}

# 爬虫设置
CRAWL_DELAY = 5  # 爬虫延迟（秒）
MAX_CONCURRENT_REQUESTS = 10  # 最大并发请求数

# 日志设置
LOG_FILE = 'proxy_harvester.log'
LOG_LEVEL = 'INFO'
