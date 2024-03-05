import asyncio

import aiohttp
from bs4 import BeautifulSoup
from sqlalchemy import Result, select

from dobrotsen.config import hidden
from dobrotsen.crud import write_data, get_links_from_db
from dobrotsen.models import Dobrotsen

from engine import db
from func import get_html, ua


async def write_dobrotsen_menu(url):
    print('Configure menu')
    menu = dict()
    html_code = await get_html(url=url, city_id=hidden.city_id)
    soup = BeautifulSoup(html_code, 'lxml')
    block = soup.find_all(name='div', attrs={'class': 'catalog-block'})
    city = soup.find(name='div', attrs={'class': 'header-location js-popup-open'})
    for b in block:
        if b.getText().strip():
            parent_title = b.findChildren(name="a", attrs={'class': 'catalog-block-title'}, recursive=False)
            childs_title = b.findChildren(name="a", attrs={'class': 'catalog-item'}, recursive=False)
            menu.update(
                {
                    parent_title[0].getText().strip(): {
                        'link': parent_title[0].get('href'),
                        'child': dict(
                            zip(
                                [i.getText().strip() for i in childs_title],
                                [i.get('href') for i in childs_title]
                            )
                        )
                    }
                }
            )
    values = list()
    for key, value in menu.items():
        values.append(
            {
                'parent': 0,
                'title': key,
                'link': f"https://dobrotsen.ru{value.get('link')}"
            }
        )
    async with db.scoped_session() as session:
        await write_data(session=session, table=Dobrotsen, data=values)
    values.clear()
    async with db.scoped_session() as session:
        result: Result = await session.execute(select(Dobrotsen).filter(Dobrotsen.parent == 0))
        r = result.scalars().all()
        dict_parent = {
            k: v for k, v in zip([i.title for i in r], [i.id for i in r])
        }
        for key, value in menu.items():
            for k, v in value.get('child').items():
                values.append(
                    {
                        'parent': dict_parent.get(key),
                        'title': k,
                        'link': f"https://dobrotsen.ru{v}"
                    }
                )
        await write_data(session=session, table=Dobrotsen, data=values)


async def bs_page_processing(page_html: str, parent: int):
    result = list()
    soup = BeautifulSoup(page_html, 'lxml')
    titles = soup.find_all(name='div', attrs={'class': 'products-item-title'})
    prices = soup.find_all(name='span', attrs={'itemprop': 'price'})
    links = soup.find_all(name='a', attrs={'class': 'products-item-image'})
    images = soup.find_all(name='img', attrs={'itemprop': 'image'})
    for title, price, link, image in zip(titles, prices, links, images):
        result.append(
            {
                'parent': parent,
                'title': title.getText().strip().strip(),
                'link': f"https://dobrotsen.ru{link.get('href')}",
                'price': float(price.getText().rsplit(' ', 1)[0].replace('\xa0', '')),
                'image': f"https://dobrotsen.ru{image.get('src')}"
            }
        )
    if titles:
        async with db.scoped_session() as session:
            await write_data(session=session, table=Dobrotsen, data=result)


async def pars_links():
    print('Start parsing')
    async with db.scoped_session() as session:
        links = await get_links_from_db(session=session, table=Dobrotsen)
    cookies = {"CITY_ID": hidden.city_id, 'CITY_CONFIRMED': 'Y', }
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False),
                                     cookies=cookies) as session:
        for link, parent in links.items():
            print(link)
            async with session.get(url=link,
                                   headers={
                                       'user-agent': ua.random
                                   }
                                   ) as response:
                html_code = await response.text()
            await bs_page_processing(page_html=html_code, parent=parent)
            await asyncio.sleep(1)
