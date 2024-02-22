import asyncio

import aiohttp
from fake_useragent import UserAgent
from bs4 import BeautifulSoup

ua = UserAgent()

link = 'https://dobrotsen.ru/catalog/'


async def main():
    async with aiohttp.ClientSession() as session:
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
    d = {k: v for k, v in zip(categories, links)}
    for k, v in d.items():
        print(f'{k}: {v}')


if __name__ == "__main__":
    asyncio.run(main())
