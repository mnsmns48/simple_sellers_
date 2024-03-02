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
                'link': value.get('link')
            }
        )
    async with db.scoped_session() as session:
        await write_data(session=session, table=Dobrotsen, data=values)
    values.clear()
    async with db.scoped_session() as session:
        result: Result = await session.execute(select(Dobrotsen).filter(Dobrotsen.parent == 0))
        r = result.scalars().all()
        dict_parent = {
            k: v for k, v in zip(
                [i.title for i in r],
                [i.id for i in r]
            )
        }
        for key, value in menu.items():
            for k, v in value.get('child').items():
                values.append(
                    {
                        'parent': dict_parent.get(key),
                        'title': k,
                        'link': v
                    }
                )
        await write_data(session=session, table=Dobrotsen, data=values)


async def pars_links():
    # async with db.scoped_session() as session:
    #     links = await get_links_from_db(session=session, table=Dobrotsen)
    # links = list(links.keys())
    links = ['/catalog/zamorozhennye-produkty/myaso/']
    cookies = {"CITY_ID": hidden.city_id, 'CITY_CONFIRMED': 'Y', }
    async with aiohttp.ClientSession(cookies=cookies) as session:
        for link in links:
            async with session.get(url=f'https://dobrotsen.ru{link}',
                                   headers={
                                       'user-agent': ua.random
                                   }
                                   ) as response:
                html_code = await response.text()
                print(html_code)

