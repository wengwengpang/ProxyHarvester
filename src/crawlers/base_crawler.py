import requests
from abc import ABC, abstractmethod
import random
import time
from typing import List, Dict
from src.crawlers.proxy_sources import get_available_sources

class BaseCrawler(ABC):
    """
    基础爬虫类，定义了爬虫的基本结构和通用方法
    """

    def __init__(self):
        self.session = requests.Session()
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
            # 添加更多User-Agent
        ]
        self.sources = get_available_sources()

    def get_random_user_agent(self) -> str:
        """
        随机选择一个User-Agent
        """
        return random.choice(self.user_agents)

    def get_next_source(self):
        """
        获取下一个可用的代理源
        """
        if self.sources:
            return self.sources.pop(0)
        else:
            self.sources = get_available_sources()
            return self.sources.pop(0) if self.sources else None

    def make_request(self, url: str, method: str = "GET", **kwargs) -> requests.Response:
        """
        发送HTTP请求并处理可能的异常
        """
        try:
            headers = kwargs.pop("headers", {})
            headers["User-Agent"] = self.get_random_user_agent()
            response = self.session.request(method, url, headers=headers, timeout=10, **kwargs)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            print(f"请求失败: {url}, 错误: {str(e)}")
            return None

    @abstractmethod
    def crawl(self) -> List[Dict[str, str]]:
        """
        爬取代理IP的抽象方法，需要被子类实现
        """
        pass

    def respect_robots_txt(self, url: str) -> bool:
        """
        检查robots.txt，确保爬取是被允许的
        """
        robots_url = f"{url.split('//', 1)[0]}//{url.split('//', 1)[1].split('/', 1)[0]}/robots.txt"
        response = self.make_request(robots_url)
        if response and "User-agent: *" in response.text and "Disallow: /" in response.text:
            return False
        return True

    def crawl_with_delay(self) -> List[Dict[str, str]]:
        """
        带有延迟的爬取方法，以降低被封禁的风险
        """
        source = self.get_next_source()
        if not source:
            print("没有可用的代理源")
            return []

        if not self.respect_robots_txt(source['url']):
            print(f"根据robots.txt，不允许爬取 {source['url']}")
            return []
        
        proxies = self.crawl(source['url'])
        time.sleep(random.uniform(1, 3))  # 随机延迟1-3秒
        return proxies
