import asyncio

import aiohttp
from fake_useragent import UserAgent
from bs4 import BeautifulSoup

ua = UserAgent()

link = 'https://dobrotsen.ru/catalog/'


async def start():
    cookies = {"CITY_ID": '181830', 'CITY_CONFIRMED': 'Y', }
    async with aiohttp.ClientSession(cookies=cookies) as session:
        async with session.get(url=link,
                               headers={
                                   'user-agent': ua.random
                               }
                               ) as response:
            html_code = await response.text()
    soup = BeautifulSoup(html_code, 'lxml')
    block = soup.find_all(name='a', attrs={'class': 'catalog-block-title'})
    categories = [item.getText().strip() for item in block if item.getText().strip() != '']
    links = [item.get('href') for item in block if item.get('href') != '']
    city = soup.find(name='div', attrs={'class': 'header-location js-popup-open'})
    d = {k: v for k, v in zip(categories, links)}
    for k, v in d.items():
        print(f'{k}: {v}')
    print(city.getText().strip())
