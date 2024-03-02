import aiohttp
from fake_useragent import UserAgent

ua = UserAgent()


async def get_html(url: str, city_id: str) -> str:
    cookies = {"CITY_ID": city_id, 'CITY_CONFIRMED': 'Y', }
    async with aiohttp.ClientSession(cookies=cookies) as session:
        async with session.get(url=url,
                               headers={
                                   'user-agent': ua.random
                               }
                               ) as response:
            html_code = await response.text()
    return html_code