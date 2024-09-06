import unittest
import asyncio
from src.proxy_checker import ProxyChecker

class TestProxyChecker(unittest.TestCase):
    def setUp(self):
        self.checker = ProxyChecker()

    def test_check_proxy(self):
        proxy = {
            'ip': '127.0.0.1',
            'port': '8080',
            'protocol': 'http'
        }
        result = asyncio.run(self.checker.check_proxy(proxy))
        self.assertIn('is_valid', result)

    def test_check_proxies(self):
        proxies = [
            {'ip': '127.0.0.1', 'port': '8080', 'protocol': 'http'},
            {'ip': '127.0.0.1', 'port': '8081', 'protocol': 'https'}
        ]
        results = asyncio.run(self.checker.check_proxies(proxies))
        self.assertEqual(len(results), 2)
        for result in results:
            self.assertIn('is_valid', result)

if __name__ == '__main__':
    unittest.main()
