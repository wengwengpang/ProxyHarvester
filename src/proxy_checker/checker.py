import aiohttp
import asyncio
from typing import List, Dict

class ProxyChecker:
    """
    代理检查器类，用于验证代理的可用性和性能
    """

    def __init__(self, test_url: str = "http://httpbin.org/ip"):
        self.test_url = test_url

    async def check_proxy(self, proxy: Dict[str, str]) -> Dict[str, str]:
        """
        异步检查单个代理的可用性和延迟
        """
        start_time = asyncio.get_event_loop().time()
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.test_url, proxy=f"{proxy['protocol']}://{proxy['ip']}:{proxy['port']}", timeout=10) as response:
                    if response.status == 200:
                        end_time = asyncio.get_event_loop().time()
                        proxy['latency'] = end_time - start_time
                        proxy['speed'] = len(await response.text()) / proxy['latency']  # 简单的速度估算
                        proxy['is_valid'] = True
                        return proxy
        except Exception as e:
            print(f"代理检查失败: {proxy['ip']}:{proxy['port']}, 错误: {str(e)}")
        
        proxy['is_valid'] = False
        return proxy

    async def check_proxies(self, proxies: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """
        异步检查多个代理
        """
        tasks = [self.check_proxy(proxy) for proxy in proxies]
        return await asyncio.gather(*tasks)

    def run_check(self, proxies: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """
        运行代理检查
        """
        return asyncio.run(self.check_proxies(proxies))
