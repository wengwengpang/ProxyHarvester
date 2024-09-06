from .base_crawler import BaseCrawler
from bs4 import BeautifulSoup
from typing import List, Dict

class ProxyNovaCrawler(BaseCrawler):
    """
    专门用于爬取 proxynova.com 网站的爬虫类
    """

    def crawl(self, url: str) -> List[Dict[str, str]]:
        """
        爬取 proxynova.com 网站的代理IP
        """
        response = self.make_request(url)
        if not response:
            return []

        soup = BeautifulSoup(response.text, 'html.parser')
        proxies = []
        for row in soup.select('table#tbl_proxy_list tbody tr'):
            cols = row.find_all('td')
            if len(cols) >= 7:
                proxy = {
                    'ip': cols[0].text.strip(),
                    'port': cols[1].text.strip(),
                    'country': cols[5].text.strip(),
                    'anonymity': cols[6].text.strip(),
                    'https': 'unknown',
                    'last_checked': cols[7].text.strip() if len(cols) > 7 else 'unknown',
                    'provider': 'proxynova.com'
                }
                proxies.append(proxy)
        return proxies
