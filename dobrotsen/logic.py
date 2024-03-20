import asyncio
from datetime import datetime
import aiohttp
from bs4 import BeautifulSoup
from sqlalchemy import Result, select, text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.decl_api import DeclarativeAttributeIntercept

from config import dobrotsen_settings
from crud import write_data
from dobrotsen.models_dobrotsen import Dobrotsen

from engine import dobrotsen_db
from func import ua, get_html


async def write_dobrotsen_menu(url):
    print('Configure menu')
    menu = dict()
    cookies = {"CITY_ID": dobrotsen_settings.city_id, 'CITY_CONFIRMED': 'Y', }
    html_code = await get_html(url=url, cookies=cookies)
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
    async with dobrotsen_db.scoped_session() as session:
        await write_data(session=session, table=Dobrotsen, data=values)
    values.clear()
    async with dobrotsen_db.scoped_session() as session:
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
        async with dobrotsen_db.scoped_session() as session:
            await write_data(session=session, table=Dobrotsen, data=result)


async def pars_links():
    print('Start parsing')
    async with dobrotsen_db.scoped_session() as session:
        links = await get_links_from_db(session=session, table=Dobrotsen)
    cookies = {"CITY_ID": dobrotsen_settings.city_id, 'CITY_CONFIRMED': 'Y', }
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
    print('Database updated:', datetime.now())


async def get_links_from_db(session: AsyncSession, table: DeclarativeAttributeIntercept) -> dict:
    result_dict = dict()
    subq1 = select(table.parent).scalar_subquery()
    q1 = select(table.link, table.id).filter(table.id.not_in(subq1))
    q2 = select(table.link, table.id).filter(table.parent != 0)
    query = q1.union(q2).order_by(text("1"))
    result: Result = await session.execute(query)
    for line in result.fetchall():
        result_dict.update(
            {
                line[0]: line[1]
            }
        )
    return result_dict
