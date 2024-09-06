import unittest
import tempfile
import os
from src.database import DBManager

class TestDBManager(unittest.TestCase):
    def setUp(self):
        self.temp_db = tempfile.NamedTemporaryFile(delete=False)
        self.db_manager = DBManager(self.temp_db.name)

    def tearDown(self):
        self.temp_db.close()
        os.unlink(self.temp_db.name)

    def test_add_and_get_proxy(self):
        proxy = {
            'ip': '127.0.0.1',
            'port': 8080,
            'protocol': 'http',
            'country': 'US',
            'anonymity': 'high',
            'speed': 1.5,
            'latency': 0.5,
            'is_valid': True
        }
        self.db_manager.add_proxy(proxy)
        
        proxies = self.db_manager.get_all_proxies()
        self.assertEqual(len(proxies), 1)
        self.assertEqual(proxies[0]['ip'], proxy['ip'])

    def test_delete_proxy(self):
        proxy = {
            'ip': '127.0.0.1',
            'port': 8080,
            'protocol': 'http',
            'country': 'US',
            'anonymity': 'high',
            'speed': 1.5,
            'latency': 0.5,
            'is_valid': True
        }
        self.db_manager.add_proxy(proxy)
        proxies = self.db_manager.get_all_proxies()
        self.assertEqual(len(proxies), 1)

        self.db_manager.delete_proxy(proxies[0]['id'])
        proxies = self.db_manager.get_all_proxies()
        self.assertEqual(len(proxies), 0)

if __name__ == '__main__':
    unittest.main()
