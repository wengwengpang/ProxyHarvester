import unittest
from src.crawlers import FreeProxyListCrawler, ProxyNovaCrawler

class TestCrawlers(unittest.TestCase):
    def test_free_proxy_list_crawler(self):
        crawler = FreeProxyListCrawler()
        proxies = crawler.crawl('https://free-proxy-list.net/')
        self.assertIsInstance(proxies, list)
        if proxies:
            self.assertIsInstance(proxies[0], dict)
            self.assertIn('ip', proxies[0])
            self.assertIn('port', proxies[0])

    def test_proxy_nova_crawler(self):
        crawler = ProxyNovaCrawler()
        proxies = crawler.crawl('https://www.proxynova.com/proxy-server-list/')
        self.assertIsInstance(proxies, list)
        if proxies:
            self.assertIsInstance(proxies[0], dict)
            self.assertIn('ip', proxies[0])
            self.assertIn('port', proxies[0])

if __name__ == '__main__':
    unittest.main()
