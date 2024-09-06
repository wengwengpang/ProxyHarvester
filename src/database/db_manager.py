import sqlite3
from contextlib import contextmanager
from typing import List, Dict
import bcrypt

class DBManager:
    """
    数据库管理器类，负责与SQLite数据库的交互
    """

    def __init__(self, db_path: str):
        self.db_path = db_path
        self.init_db()

    @contextmanager
    def get_connection(self):
        """
        创建数据库连接的上下文管理器
        """
        conn = sqlite3.connect(self.db_path)
        try:
            yield conn
        finally:
            conn.close()

    def init_db(self):
        """
        初始化数据库，创建必要的表
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS proxies (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    ip TEXT NOT NULL,
                    port INTEGER NOT NULL,
                    protocol TEXT NOT NULL,
                    country TEXT,
                    anonymity TEXT,
                    speed REAL,
                    latency REAL,
                    is_valid BOOLEAN,
                    last_checked TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL UNIQUE,
                    password TEXT NOT NULL
                )
            ''')
            conn.commit()

    def add_proxy(self, proxy: Dict[str, str]):
        """
        向数据库中添加新的代理
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO proxies (ip, port, protocol, country, anonymity, speed, latency, is_valid)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (proxy['ip'], proxy['port'], proxy['protocol'], proxy['country'],
                  proxy['anonymity'], proxy['speed'], proxy['latency'], proxy['is_valid']))
            conn.commit()

    def get_all_proxies(self) -> List[Dict[str, str]]:
        """
        从数据库获取所有代理
        """
        with self.get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM proxies ORDER BY latency ASC')
            return [dict(row) for row in cursor.fetchall()]

    def get_all_valid_proxies(self) -> List[Dict[str, str]]:
        """
        从数据库获取所有有效的代理
        """
        with self.get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM proxies WHERE is_valid = 1 ORDER BY latency ASC')
            return [dict(row) for row in cursor.fetchall()]

    def delete_proxy(self, proxy_id: int):
        """
        从数据库中删除指定的代理
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM proxies WHERE id = ?', (proxy_id,))
            conn.commit()

    def update_proxy(self, proxy_id: int, proxy: Dict[str, str]):
        """
        更新数据库中的代理信息
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE proxies
                SET ip=?, port=?, protocol=?, country=?, anonymity=?, speed=?, latency=?, is_valid=?, last_checked=CURRENT_TIMESTAMP
                WHERE id=?
            ''', (proxy['ip'], proxy['port'], proxy['protocol'], proxy['country'],
                  proxy['anonymity'], proxy['speed'], proxy['latency'], proxy['is_valid'], proxy_id))
            conn.commit()

    def add_user(self, username: str, password: str):
        """
        添加新用户
        """
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)',
                           (username, hashed_password))
            conn.commit()

    def verify_user(self, username: str, password: str) -> bool:
        """
        验证用户登录
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT password FROM users WHERE username = ?', (username,))
            result = cursor.fetchone()
            if result:
                return bcrypt.checkpw(password.encode('utf-8'), result[0])
        return False

    def get_user(self, username: str) -> Dict[str, str]:
        """
        获取用户信息
        """
        with self.get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
            result = cursor.fetchone()
            return dict(result) if result else None
