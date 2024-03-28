import asyncio
from datetime import datetime, date, timedelta

import pandas as pd
from bs4 import BeautifulSoup
from sqlalchemy import select, Result

from alterainvest.models_altera import AlteraModel, Data
from config import altera_settings
from crud import write_data, get_data
from engine import altera_db
from func import get_html

today = date.today()


async def get_altera_links():
    result = list()
    data = await get_html('https://alterainvest.ru/rus/')
    soup = BeautifulSoup(markup=data, features='lxml')
    table = soup.find('div', {'class': 'col-8'})
    items = table.find_all('a', {'class': 'al-subcategory__link'})
    for item in items:
        result.append({
            'category': item.text.split('\t\t\t\t\t\t\t\t\t\t\t\t\t\t')[0],
            'link': f"https://alterainvest.ru{item.get('href')}"
        })
    async with altera_db.scoped_session() as session:
        await write_data(session=session,
                         table=AlteraModel.metadata.tables.get(altera_settings.table_links),
                         data=result)


async def altera_pars():
    async with altera_db.scoped_session() as session:
        links_data = await get_data(session=session, table=AlteraModel.metadata.tables.get(altera_settings.table_links))
    for line in links_data:
        count = 1
        while True:
            url = line[2] if count == 1 else f"{line[2]}page-{count}/"
            page_data = await get_html(url)
            result = await altera_bs4_process(html=page_data, category=line[1])
            if result.get('exit'):
                break
            else:
                print(result.get('data'))
                count += 1
                async with altera_db.scoped_session() as session:
                    await write_data(session=session,
                                     table=AlteraModel.metadata.tables.get(altera_settings.table_data),
                                     data=result.get('data'))
            await asyncio.sleep(2)


async def altera_bs4_process(html: str, category: str) -> dict:
    result_dict = dict()
    result = list()
    soup = BeautifulSoup(markup=html, features='lxml')
    catalog = soup.find('div', {'class': 'al-catalog'})
    items = catalog.find_all('div', {'class': 'col-4'})
    for item in items:
        span_p3 = item.find_all('span', {'class': ['p3', 'color--black']})
        city = item.find_all('span', {'class': ['caption', 'color--mid-gray', 'df', 'aic', 'mr8']})[0].text
        try:
            date_ = datetime.strptime(
                item.find_all('span', {'class':
                                           ['caption', 'color--mid-gray', 'df', 'aic', 'mr8']}
                              )[1].text, " %d.%m.%Y ").date()

            if today - timedelta(days=altera_settings.period) <= date_:
                result.append({
                    'category': category,
                    'title': item.find('span', {'class': ['heading5', 'mb4', 'db', 'link--black']}).text,
                    'city': city,
                    'date': date_,
                    'price': item.find('div', {'class': ['heading6', 'mb4', 'db', 'color--main']}).text,
                    'profit': [i.text.strip() for i in span_p3[1:6:2][0]][0],
                    'payback': [i.text.strip() for i in span_p3[1:6:2][1]][0],
                    'confirm': [i.text.strip() for i in span_p3[1:6:2][2]][0],
                    'link': f"https://alterainvest.ru{item.find('a').get('href')}",
                })
        except ValueError:
            result_dict.update({
                'exit': False if len(result) > 0 else True,
                'data': result
            })
            return result_dict
    result_dict.update({
        'exit': False if len(result) > 0 else True,
        'data': result
    })
    return result_dict


async def altera_output():
    query = select(Data.id,
                   Data.category,
                   Data.title,
                   Data.city,
                   Data.date,
                   Data.price,
                   Data.profit,
                   Data.payback,
                   Data.confirm,
                   Data.link).order_by(Data.category, Data.city, Data.date.desc())
    async with altera_db.scoped_session() as session:
        data: Result = await session.execute(query)
        result = data.all()
    df = pd.DataFrame(result)
    filename = f'altera_{altera_settings.table_data}_{today}.xlsx'
    writer = pd.ExcelWriter(filename)
    try:
        df.to_excel(writer, index=False)
    finally:
        writer.close()
        print(f'Ready')
