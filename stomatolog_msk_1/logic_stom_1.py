import re

from bs4 import BeautifulSoup

from config import stomat_settings
from crud import write_data, del_data
from engine import stomat_db
from func import get_html
from stomatolog_msk_1.models_stomatology import StomatBase


async def martirosyan_pro(links: list):
    result_dict = list()
    for url in links[:1]:
        html = await get_html(url)
        soup = BeautifulSoup(markup=html, features='lxml')
        parents = soup.find_all(name='div', attrs={'class': 't849__wrapper'})
        for parent in parents:
            childs = [c.getText() for c in parent.findChildren('li')]
            if len(childs) > 0:
                for c in childs:
                    regex = re.compile(r'\d{1,3}.\d00')
                    result_dict.append({
                        'company': 'Клиника Артура Мартиросяна',
                        'address': 'Большой Саввинский переулок дом 12с6',
                        'site': 'https://martirosyan.pro/',
                        'category': parent.span.contents[0].get_text(),
                        'med_service': re.split(regex, c)[0],
                        'price': regex.findall(c)[0] + '₽' if regex.findall(c) else c
                    })
            else:
                result_dict.append({
                    'company': 'Клиника Артура Мартиросяна',
                    'address': 'Большой Саввинский переулок дом 12с6',
                    'site': 'https://martirosyan.pro/',
                    'category': parent.span.contents[0].get_text(),
                    'med_service': parent.span.contents[0].get_text(),
                    'price': parent.span.contents[1].get_text(),
                })
    async with stomat_db.scoped_session() as session:
        await write_data(session=session, table=StomatBase.metadata.tables.get(stomat_settings.tablename),
                         data=result_dict)


async def familydoctor(links: list):
    result_dict = list()
    for url in links:
        html = await get_html(url)
        soup = BeautifulSoup(markup=html, features='lxml')
        regex = re.compile('price_item_')
        titles = soup.find_all(name='tr', attrs={'data-id': regex})
        for line in titles:
            result_dict.append({
                'company': 'Клиника "Семейный доктор"',
                'address': 'Корпус на Усачева (для взрослых и детей) (м. Спортивная) '
                           'Корпус на Усачева (для взрослых и детей) (м. Спортивная) '
                           'Корпус на Новослободской (для взрослых и детей) (м. Новослободская) '
                           'Корпус на Озерковской (для взрослых) (м. Новокузнецкая) '
                           'Корпус на Бауманской (для взрослых) (м. Бауманская)',
                'site': 'https://familydoctor.ru',
                'category': f"[{soup.find(name='div', attrs={'class': 'item sel'}).text.strip()}] "
                            f"{soup.find(name='h1').text.strip()}",
                'med_service': line.td.text,
                'price': line.find_next('td', attrs={'data-label-before': 'Стоимость '}).text,
                'price_promo': line.find_next('a', attrs={'class': 'price_lnk'}).text

            })
    async with stomat_db.scoped_session() as session:
        await write_data(session=session, table=StomatBase.metadata.tables.get(stomat_settings.tablename),
                         data=result_dict)


async def nydc(links: list):
    result_dict = list()
    for url in links:
        html = await get_html(url)
        soup = BeautifulSoup(markup=html, features='lxml')
        regex = re.compile('bx_3218110189_')
        parents = soup.find_all(name='div', attrs={'id': regex})
        for line in parents:
            child = line.findChildren(name='div', attrs={'class': 'item'})
            for i in child:
                result_dict.append({
                    'company': 'Нью-Йорк Дентал Центр',
                    'address': 'м. Спортивная, ул. Ефремова 14',
                    'site': 'https://nydc.ru',
                    'category': line.find('a', {'style': 'color: #000;'}).text.strip().replace('​​', ''),
                    'med_service': i.p.text,
                    'price': i.contents[3].text
                })
    async with stomat_db.scoped_session() as session:
        await write_data(session=session, table=StomatBase.metadata.tables.get(stomat_settings.tablename),
                         data=result_dict)


async def orthodont(links: list):
    result_dict = list()
    for url in links:
        html = await get_html(url)
        soup = BeautifulSoup(markup=html, features='lxml')
        table = soup.find('table', {'class': 'table table-striped table-hover js-table'})
        # regex =
        sections = soup.find_all('td', {'colspan': '3'})
        sections_numbers = [l.find_previous('tr').get('data-section') for l in sections]
        for n in sections_numbers:
            for i in table.find_all('tr', {'data-section': n})[1:]:
                title = table.find_all('tr', {'data-section': n})[:1]
                result_dict.append({
                    'company': 'Стоматология «Ортодонт-Элит»',
                    'address': 'м. Спортивная, ул. Усачева, 19Ак2',
                    'site': 'https://www.orthodont-elit.ru',
                    'category': title[0].span.text,
                    'med_service': i.td.text,
                    'price': i.strong.text
                })
    async with stomat_db.scoped_session() as session:
        await write_data(session=session, table=StomatBase.metadata.tables.get(stomat_settings.tablename),
                         data=result_dict)
        await del_data(session=session, table=StomatBase.metadata.tables.get(stomat_settings.tablename),
                       condition='-')


dependencies = {
    'https://martirosyan.pro/': {
        'links': [
            'https://martirosyan.pro/services#!/tab/504070508-1',
            'https://martirosyan.pro/services#!/tab/504070508-2',
            'https://martirosyan.pro/services#!/tab/504070508-3',
            'https://martirosyan.pro/services#!/tab/504070508-4',
            'https://martirosyan.pro/services#!/tab/504070508-5',
        ],
        'process': martirosyan_pro
    },
    'https://familydoctor.ru/prices/': {
        'links': [
            'https://familydoctor.ru/prices/stomatologiya/',
            'https://familydoctor.ru/prices/child/stomatologiya/',
            'https://familydoctor.ru/prices/ortopedicheskaya-stomatologiya/',
            'https://familydoctor.ru/prices/hirurgicheskaya-stomatologiya/',
            'https://familydoctor.ru/prices/child/hirurgicheskaya-stomatologiya/'
        ],
        'process': familydoctor
    },
    'https://nydc.ru/uslugi-i-tseny/': {
        'links': [
            'https://nydc.ru/uslugi-i-tseny/',
        ],
        'process': nydc
    },
    'https://www.orthodont-elit.ru/price/': {
        'links': [
            'https://www.orthodont-elit.ru/price/full/'
        ],
        'process': orthodont
    }
}


async def work():
    with open('stomatolog_msk_1/url_list.txt', 'r') as file:
        urls = [i.strip() for i in file.readlines()]
    for url in urls:
        site = dependencies.get(url)
        if site:
            await site.get('process')(links=site.get('links'))