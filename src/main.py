import asyncio
from src.crawlers import FreeProxyListCrawler, ProxyNovaCrawler
from src.proxy_checker import ProxyChecker
from src.database import DBManager
from src.utils import ConsoleDisplay
from config import DATABASE_PATH, INITIAL_USER

async def main():
    db_manager = DBManager(DATABASE_PATH)
    console_display = ConsoleDisplay()
    proxy_checker = ProxyChecker()

    # 初始化数据库和用户（如果不存在）
    db_manager.init_db()
    if not db_manager.get_user(INITIAL_USER['username']):
        db_manager.add_user(INITIAL_USER['username'], INITIAL_USER['password'])

    crawlers = [FreeProxyListCrawler(), ProxyNovaCrawler()]

    while True:
        for crawler in crawlers:
            proxies = crawler.crawl_with_delay()
            console_display.add_crawl_info(f"从 {crawler.__class__.__name__} 爬取到 {len(proxies)} 个代理")

            valid_proxies = await proxy_checker.check_proxies(proxies)
            
            success_count = len([p for p in valid_proxies if p['is_valid']])
            fail_count = len(proxies) - success_count
            console_display.update_stats(len(proxies), success_count, fail_count, 0)

            for proxy in valid_proxies:
                if proxy['is_valid']:
                    db_manager.add_proxy(proxy)

            console_display.display(valid_proxies)

        await asyncio.sleep(3600)  # 每小时更新一次

if __name__ == "__main__":
    asyncio.run(main())
