import ping3
from typing import List, Dict

PROXY_SOURCES = [
    {"name": "Free Proxy List", "url": "https://free-proxy-list.net/"},
    {"name": "ProxyNova", "url": "https://www.proxynova.com/proxy-server-list/"},
    {"name": "Proxy-List", "url": "https://www.proxy-list.download/HTTP"},
    {"name": "SSLProxies", "url": "https://www.sslproxies.org/"},
    {"name": "US-Proxy", "url": "https://www.us-proxy.org/"},
    {"name": "Xroxy", "url": "https://www.xroxy.com/free-proxy-lists/"},
    {"name": "HideMyName", "url": "https://hidemy.name/en/proxy-list/"},
    {"name": "ProxyList+", "url": "https://list.proxylistplus.com/Fresh-HTTP-Proxy-List-1"},
    {"name": "GatherProxy", "url": "http://www.gatherproxy.com/"},
    {"name": "PubProxy", "url": "http://pubproxy.com/api/proxy?limit=20&format=txt&type=http"}
]

def check_source_availability(source: Dict[str, str]) -> bool:
    """
    检查代理源是否可用
    """
    try:
        response_time = ping3.ping(source['url'].split('//')[1].split('/')[0])
        return response_time is not None and response_time < 2  # 假设响应时间小于2秒为可用
    except:
        return False

def get_available_sources() -> List[Dict[str, str]]:
    """
    获取所有可用的代理源
    """
    return [source for source in PROXY_SOURCES if check_source_availability(source)]
