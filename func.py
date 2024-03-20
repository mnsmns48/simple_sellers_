import aiohttp
from fake_useragent import UserAgent

ua = UserAgent()


async def get_html(url: str, **kwargs) -> str:
    cookies = kwargs.get('cookies')
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False),
                                     cookies=cookies) as session:
        async with session.get(url=url,
                               headers={
                                   'user-agent': ua.random
                               }
                               ) as response:
            html_code = await response.text()
    return html_code
