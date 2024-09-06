from colorama import Fore, Back, Style, init
from tabulate import tabulate
import os

init(autoreset=True)

class ConsoleDisplay:
    def __init__(self):
        self.crawled_count = 0
        self.success_count = 0
        self.fail_count = 0
        self.error_count = 0
        self.crawl_info = []

    def update_stats(self, crawled: int, success: int, fail: int, error: int):
        self.crawled_count += crawled
        self.success_count += success
        self.fail_count += fail
        self.error_count += error

    def add_crawl_info(self, info: str):
        self.crawl_info.append(info)
        if len(self.crawl_info) > 10:
            self.crawl_info.pop(0)

    def display(self, proxies: list):
        os.system('cls' if os.name == 'nt' else 'clear')
        self._display_crawl_info()
        self._display_stats()
        self._display_proxies(proxies)

    def _display_crawl_info(self):
        print(Fore.CYAN + "最新爬取信息:")
        for info in self.crawl_info:
            print(info)

    def _display_stats(self):
        print("\n\n" + Fore.CYAN + "统计信息:")
        print(f"{Fore.GREEN}成功代理数量: {self.success_count}")
        print(f"{Fore.RED}失败代理数量: {self.fail_count}")
        print(f"{Fore.YELLOW}错误连接数量: {self.error_count}")
        print(f"{Fore.BLUE}总爬取数量: {self.crawled_count}")

    def _display_proxies(self, proxies: list):
        print("\n\n" + Fore.GREEN + "成功的代理信息:")
        headers = ["IP", "端口", "延迟(ms)", "速度(Mbps)", "协议", "质量", "地区", "提供商"]
        table_data = [
            [
                proxy['ip'],
                proxy['port'],
                f"{proxy['latency']*1000:.2f}",
                f"{proxy['speed']:.2f}",
                proxy['protocol'],
                proxy['quality'],
                proxy['country'],
                proxy['provider']
            ] for proxy in sorted(proxies, key=lambda x: x['latency'])
        ]
        table = tabulate(table_data, headers=headers, tablefmt="fancy_grid")
        print(Fore.YELLOW + Style.BRIGHT + table)
