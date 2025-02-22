"""
@Author: Shine_Light
@Version: 1.0
@Date: 2022/3/24 20:52
"""
import httpx
from nonebot import get_driver


proxy = get_driver().config.proxy


async def get_img_bytes(url: str) -> bytes:
    async with httpx.AsyncClient(verify=False, timeout=10) as client:
        r = await client.get(url)
    return r.content


async def match_30X(url_source: str) -> str:
    """捕获30X后的网址"""
    async with httpx.AsyncClient(verify=False, timeout=10) as client:
        r = await client.get(url_source)
    try:
        url = r.headers['Location']
    except:
        try:
            url = r.next_request.url
        except:
            return url_source
    return url


def get_proxy():
    print(str.replace(proxy, "x", ""))
    if proxy and str.replace(proxy, "x", "") != "":
        proxies = {
            "http": "http://" + proxy,
            "https": "http://" + proxy
        }
        return proxies
    return None
