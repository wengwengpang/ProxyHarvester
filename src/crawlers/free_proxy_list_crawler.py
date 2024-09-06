from .base_crawler import BaseCrawler
from bs4 import BeautifulSoup
from typing import List, Dict

class FreeProxyListCrawler(BaseCrawler):
    """
    专门用于爬取 free-proxy-list.net 网站的爬虫类
    """

    def crawl(self, url: str) -> List[Dict[str, str]]:
        """
        爬取 free-proxy-list.net 网站的代理IP
        """
        response = self.make_request(url)
        if not response:
            return []

        soup = BeautifulSoup(response.text, 'html.parser')
        proxies = []
        for row in soup.select('table.table tbody tr'):
            cols = row.find_all('td')
            if len(cols) >= 8:
                proxy = {
                    'ip': cols[0].text.strip(),
                    'port': cols[1].text.strip(),
                    'country': cols[3].text.strip(),
                    'anonymity': cols[4].text.strip(),
                    'https': 'yes' if cols[6].text.strip() == 'yes' else 'no',
                    'last_checked': cols[7].text.strip(),
                    'provider': 'free-proxy-list.net'
                }
                proxies.append(proxy)
        return proxies
