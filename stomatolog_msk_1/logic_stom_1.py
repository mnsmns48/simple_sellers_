import asyncio
import os
import re
from pathlib import Path

import tabula
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By

from config import stomat_settings
from crud import write_data, del_data
from engine import stomat_db
from func import get_html
from stomatolog_msk_1.models_stomatology import StomatBase
import undetected_chromedriver as uc

path = Path(os.path.abspath(__file__)).parent.parent


async def martirosyan_pro(links: list) -> None:
    result_dict = list()
    for url in links:
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


async def familydoctor(links: list) -> None:
    result_dict = list()
    for url in links:
        html = await get_html(url)
        soup = BeautifulSoup(markup=html, features='lxml')
        regex = re.compile('price_item_')
        titles = soup.find_all(name='tr', attrs={'data-id': regex})
        for line in titles:
            result_dict.append({
                'company': 'Клиника "Семейный доктор"',
                'address': 'Баррикадная ул., 19, стр. 3',
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


async def nydc(links: list) -> None:
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


async def orthodont(links: list) -> None:
    result_dict = list()
    for url in links:
        html = await get_html(url)
        soup = BeautifulSoup(markup=html, features='lxml')
        table = soup.find('table', {'class': 'table table-striped table-hover js-table'})
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


async def alfaclinic(links: list) -> None:
    result_dict = list()
    for url in links:
        html = await get_html(url)
        soup = BeautifulSoup(markup=html, features='lxml')
        table = soup.find_all('table', {'align': 'left'})
        for item in table:
            category = item.td.text
            for i in item.findChildren('tr')[2:]:
                result_dict.append({
                    'company': 'Стоматология ALFA-CLINIC',
                    'address': 'ул. Малая Пироговская, 16',
                    'site': 'https://www.alfa-clinic.ru/',
                    'category': category,
                    'med_service': i.contents[0].text,
                    'price': i.contents[1].text,
                })
    async with stomat_db.scoped_session() as session:
        await write_data(session=session, table=StomatBase.metadata.tables.get(stomat_settings.tablename),
                         data=result_dict)


async def dentalfantasy(links: list) -> None:
    result_dict = list()
    for url in links:
        html = await get_html(url)
        soup = BeautifulSoup(markup=html, features='lxml')
        table = soup.find('div', {'class': ['py-4', 'py-md-5', 'mb-last-0 ']})
        card_list = [i.find_parent('div') for i in table.find_all('div', {'role': 'tabpanel'})]
        for item in card_list:
            category = item.find('span', {'class': ['text-body', 'state-color-switch']}).text
            for srv, price in zip(item.find_all('div', {'class': 'media-body'}),
                                  item.find_all('div', {'class': 'text-right'})):
                result_dict.append({
                    'company': 'Дентал Фэнтези',
                    'address': 'ул. Ефремова, д. 10, к. 2',
                    'site': 'https://www.dentalfantasy.ru',
                    'category': category,
                    'med_service': srv.span.text.replace('i', '').strip(),
                    'price': price.text.strip()})
    async with stomat_db.scoped_session() as session:
        await write_data(session=session, table=StomatBase.metadata.tables.get(stomat_settings.tablename),
                         data=result_dict)


async def zub_ru(links: list) -> None:
    result_dict = list()
    for url in links:
        html = await get_html(url)
        soup = BeautifulSoup(markup=html, features='lxml')
        titles = soup.find_all('h3', {'class': 'main-title-table'})
        for title in titles:
            tbody = title.find_next('div')
            for item in tbody.findChildren('tr'):
                result_dict.append({
                    'company': 'Стоматология «Зуб.ру»',
                    'address': 'м. Шаболовская, 2-й Верхний Михайловский проезд, д. 9, стр. 2, 3 этаж.',
                    'site': 'https://zub.ru/',
                    'category': title.text.strip(),
                    'med_service': item.contents[1].text.strip(),
                    'price': item.contents[3].text.strip()
                })
    async with stomat_db.scoped_session() as session:
        await write_data(session=session, table=StomatBase.metadata.tables.get(stomat_settings.tablename),
                         data=result_dict)


async def prezi_dent(links: list) -> None:
    result_dict = list()
    for url in links:
        html = await get_html(url)
        soup = BeautifulSoup(markup=html, features='lxml')
        parents = soup.find_all('div', {'class': ['accordion__item', 'jsAccordion', 'is-open']})
        for t in parents:
            category = t.find('h2').text.strip()
            for srvs, price in zip(t.findChildren('span', ['custom-tooltip', 'jsCustomTooltip']),
                                   t.findChildren('div', {'class': 'price-list__price'})):
                result_dict.append({
                    'company': 'Стоматология «ПрезиДЕНТ» на Фрунзенской',
                    'address': 'Фрунзенская набережная, д. 44/2',
                    'site': 'https://www.prezi-dent.ru/',
                    'category': category,
                    'med_service': srvs.text.strip(),
                    'price': price.text.strip()
                })
    async with stomat_db.scoped_session() as session:
        await write_data(session=session, table=StomatBase.metadata.tables.get(stomat_settings.tablename),
                         data=result_dict)


async def mositaldent(links: list) -> None:
    result_dict = list()
    for url in links:
        html = await get_html(url)
        soup = BeautifulSoup(markup=html, features='lxml')
        table = soup.find_all('div', {'class': 'prices__dep'})
        for i in table:
            title = i.find('h3', {'class': 'title closed'})
            title_text = title.contents[0].strip().rsplit('. ', 1)[1]
            for item in i.findChildren('div', {'class': 'price-wrapper'}):
                result_dict.append({
                    'company': 'Моситалмед',
                    'address': 'Комсомольский проспект, д. 15, стр. 1',
                    'site': 'https://mositaldent.ru',
                    'category': title_text,
                    'med_service': item.contents[1].text.strip(),
                    'price': item.contents[2].text.strip()
                })
    async with stomat_db.scoped_session() as session:
        await write_data(session=session, table=StomatBase.metadata.tables.get(stomat_settings.tablename),
                         data=result_dict)


async def generation_family(links: list) -> None:
    result_dict = list()
    for url in links:
        html = await get_html(url)
        soup = BeautifulSoup(markup=html, features='lxml')
        items = soup.find_all('div', {'class': ['t812__pricelist-item__title', 't-name', 't-name_sm'],
                                      'data-redactor-toolbar': 'no'})
        for line in items:
            result_dict.append({
                'company': 'Стоматологический центр Generation',
                'address': 'Ефремова 10к1',
                'site': 'https://generation.family',
                'category': line.find_previous('h2').text.strip(),
                'med_service': line.previous.previous.text.strip(),
                'price': line.text.strip()
            })
    async with stomat_db.scoped_session() as session:
        await write_data(session=session, table=StomatBase.metadata.tables.get(stomat_settings.tablename),
                         data=result_dict)


async def docdent(links: list) -> None:
    driver = uc.Chrome(headless=False,
                       use_subprocess=False,
                       version_main=114,
                       driver_executable_path=f'{path}/chromedriver')
    result_dict = list()
    for url in links:
        driver.get(url)
        await asyncio.sleep(1)
        driver.implicitly_wait(1)
        driver.find_element(By.XPATH, "//label[@class='b-item'][1]").click()
        await asyncio.sleep(1)
        driver.find_element(By.XPATH, "//div[@class='cat-c-b-btn']").click()
        await asyncio.sleep(1)
        items = driver.find_element(By.XPATH, "//div[@class='price-data-inf-blk']")
        soup = BeautifulSoup(markup=items.get_attribute('innerHTML'), features='lxml')
        for srvs, price in zip(soup.find_all('span', {'class': 'price-data-inf-txt'}),
                               soup.find_all('span', {'class': 'price-data-buy-txt'})):
            result_dict.append({
                'company': 'DOCDENT',
                'address': 'Ломоносовский просп., 7, корп. 5',
                'site': 'https://docdent.ru',
                'med_service': srvs.text.strip(),
                'price': price.text.strip()
            })
    driver.quit()
    async with stomat_db.scoped_session() as session:
        await write_data(session=session, table=StomatBase.metadata.tables.get(stomat_settings.tablename),
                         data=result_dict)


async def alfazdrav(links: list) -> None:
    result_dict = list()
    driver = uc.Chrome(headless=False,
                       use_subprocess=False,
                       version_main=114,
                       driver_executable_path=f'{path}/chromedriver')
    for url in links:
        driver.get(url)
        await asyncio.sleep(1)
        driver.implicitly_wait(1)
        driver.find_element(By.XPATH, "//li[@class='b-content-tabs__title b-content-tabs__title--js_init'][3]").click()
        await asyncio.sleep(1)
        items = driver.find_element(By.XPATH, "//ul[@data-id='dental-department']")
        soup = BeautifulSoup(markup=items.get_attribute('innerHTML'), features='lxml')
        items = soup.find_all('li', {'class': ['b-prices__section']})
        for line in items:
            category = line.find('p', {'class': ['h3', 'b-prices__section-title']}).text.strip()
            for srvs, price in zip(line.findChildren('td', {'class': 'b-prices__item-name'}),
                                   line.findChildren('td', {'class': 'b-prices__item-price'})):
                result_dict.append({
                    'company': 'Альфа-Центр Здоровья',
                    'address': 'Комсомольский проспект, 17/11',
                    'site': 'https://alfazdrav.ru',
                    'category': category,
                    'med_service': srvs.text.strip(),
                    'price': price.text.strip()
                })
    driver.quit()
    async with stomat_db.scoped_session() as session:
        await write_data(session=session, table=StomatBase.metadata.tables.get(stomat_settings.tablename),
                         data=result_dict)
        await del_data(session=session, table=StomatBase.metadata.tables.get(stomat_settings.tablename),
                       condition='')


async def lcenter(links: list) -> None:
    result_dict = list()
    for url in links:
        html = await get_html(url)
        soup = BeautifulSoup(markup=html, features='lxml')
        for srvs, price in zip(soup.find_all('div', {'class': 'product-price--title'}),
                               soup.find_all('div', {'class': 'product-price--price'})):
            result_dict.append({
                'company': 'Лечебный центр',
                'address': 'м. Парк Культуры, ул. Тимура Фрунзе 15/1',
                'site': 'lcenter.ru',
                'med_service': srvs.text.strip().split('  ')[0].strip(),
                'price': price.text.strip()
            })
    async with stomat_db.scoped_session() as session:
        await write_data(session=session, table=StomatBase.metadata.tables.get(stomat_settings.tablename),
                         data=result_dict)


async def slavdent(links: list) -> None:
    result_dict = list()
    for url in links:
        html = await get_html(url)
        soup = BeautifulSoup(markup=html, features='lxml')
        items = soup.find_all('div', {'class': 'price-section bs-1'})
        for line in items:
            category = line.div.div.text.strip()
            for srvs, price in zip(soup.find_all('div', {'class': 'price-item__name'}),
                                   soup.findChildren('div', {'class': 'price-item__price'})):
                result_dict.append({
                    'company': 'Славдент',
                    'address': 'Комсомольский пр-т, д.35',
                    'site': 'https://slavdent.ru',
                    'category': category,
                    'med_service': srvs.text.strip(),
                    'price': price.text.strip().split('   ')[0]
                })
    async with stomat_db.scoped_session() as session:
        await write_data(session=session, table=StomatBase.metadata.tables.get(stomat_settings.tablename),
                         data=result_dict)


async def artdent(links: list) -> None:
    result_dict = list()
    for url in links:
        html = await get_html(url)
        soup = BeautifulSoup(markup=html, features='lxml')
        table = soup.find('h1')
        tds = table.find_next('table').find_all('tr')
        arr = list()
        for line in tds[1:]:
            try:
                srvs = line.contents[3].text.strip()
                price = line.contents[5].text.strip()
            except IndexError:
                srvs = line.contents[1].text.strip()
                price = line.contents[3].text.strip()
            if len(srvs) > 117 or len(price) > 7 or price == '-' or srvs == price or price == '':
                pass
            else:
                arr.append([srvs, price])
        for line in arr:
            result_dict.append({
                'company': 'Стоматология "АртДЕНТ"',
                'address': 'Хамовники, ул. Усачева, д.29, кор.3',
                'site': 'https://artdent.ru',
                'category': table.text,
                'med_service': line[0],
                'price': line[1]
            })
    async with stomat_db.scoped_session() as session:
        await write_data(session=session, table=StomatBase.metadata.tables.get(stomat_settings.tablename),
                         data=result_dict)


async def drelmar(links: list) -> None:
    result_dict = list()
    driver = uc.Chrome(headless=False,
                       use_subprocess=False,
                       version_main=114,
                       driver_executable_path=f'{path}/chromedriver')
    for url in links:
        driver.get(url)
        driver.implicitly_wait(2)
        end = driver.find_element(By.XPATH, "//div[@class='r t-rec t-rec_pt_30 t-screenmin-980px']")
        driver.execute_script("arguments[0].scrollIntoView(true);", end)
        await asyncio.sleep(1)
        table = driver.find_element(By.XPATH, "//div[@class='t585'][1]")
        soup = BeautifulSoup(markup=table.get_attribute('innerHTML'), features='lxml')
        items = soup.find_all('div', {'class': 't585__header'})
        for line in items:
            text = (line.find_next('div',
                                   {'class': ['t585__text', 't-descr', 't-descr_xs']}).text
                    .replace(' ', ' ').replace(' ', ' '))
            refactor_text = text.strip().rsplit('руб.')
            for srvs in refactor_text:
                splt = srvs.split(' —')
                if len(splt) == 2:
                    result_dict.append({
                        'company': 'Лаборатория улыбок Dr. Elmar',
                        'address': 'Оболенский переулок, д. 9, корп. 8 (м."Фрунзенская")',
                        'site': 'https://www.drelmar.ru',
                        'category': line.contents[0].text,
                        'med_service': splt[0].strip(),
                        'price': splt[1].replace('  ', ' ').strip()
                    })
    driver.quit()
    async with stomat_db.scoped_session() as session:
        await write_data(session=session, table=StomatBase.metadata.tables.get(stomat_settings.tablename),
                         data=result_dict)


async def evklaz(links: list) -> None:
    result_dict = list()
    for url in links:
        html = await get_html(url)
        soup = BeautifulSoup(markup=html, features='lxml')
        links = soup.find('table').find_all('a', href=True)
        hrefs = [f"https://evklaz-clinik.ru{i.get('href')}" for i in links]
        cat_locs = [7.980000019073486, 16.879968643188477, 9.0, 15.89999771118164]
        med_locs = [5.519999980926514]
        for href in hrefs:
            table = tabula.read_pdf(input_path=href, stream=True, pages='all', output_format="json")
            category = str()
            for line in table:
                data = line.get('data')
                for i in data:
                    if len(i) == 2:
                        height = i[0].get('height')
                        if height in cat_locs and i[1].get('text') != '':
                            category = i[0].get('text')
                        if height in med_locs and i[0].get('height') == i[1].get('height'):
                            result_dict.append({
                                'company': 'Медицинский Центр ЭВКЛАЗ',
                                'address': 'Комсомольский проспект, д. 42, стр. 2, офис 7',
                                'site': 'https://evklaz-clinik.ru',
                                'category': category.replace('цена (руб)', ''),
                                'med_service': i[0].get('text').strip(),
                                'price': i[1].get('text').strip().strip()
                            })
                        elif height == 0.0:
                            result_dict.append({
                                'company': 'Медицинский Центр ЭВКЛАЗ',
                                'address': 'Комсомольский проспект, д. 42, стр. 2, офис 7',
                                'site': 'https://evklaz-clinik.ru',
                                'category': category.replace('цена (руб)', ''),
                                'med_service': f"{data[data.index(i) - 1][0].get('text')} "
                                               f"{data[data.index(i) + 1][0].get('text')}",
                                'price': data[data.index(i)][1].get('text')
                            })
                    if len(i) == 1:
                        height = i[0].get('height')
                        if height in cat_locs:
                            category = i[0].get('text')
                        if height in med_locs:
                            try:
                                result_dict.append({
                                    'company': 'Медицинский Центр ЭВКЛАЗ',
                                    'address': 'Комсомольский проспект, д. 42, стр. 2, офис 7',
                                    'site': 'https://evklaz-clinik.ru',
                                    'category': category.replace('цена (руб)', ''),
                                    'med_service': i[0].get('text').rsplit(' ', 1)[0].strip(),
                                    'price': i[0].get('text').rsplit(' ', 1)[1].strip()
                                })
                            except IndexError:
                                pass
    async with stomat_db.scoped_session() as session:
        await write_data(session=session, table=StomatBase.metadata.tables.get(stomat_settings.tablename),
                         data=result_dict)


dependencies = {
    # 'https://martirosyan.pro/': {
    #     'links': ['https://martirosyan.pro/services#!/tab/504070508-1'],
    #     'process': martirosyan_pro
    # },
    # 'https://familydoctor.ru/prices/': {
    #     'links': [
    #         'https://familydoctor.ru/prices/stomatologiya/',
    #         'https://familydoctor.ru/prices/child/stomatologiya/',
    #         'https://familydoctor.ru/prices/ortopedicheskaya-stomatologiya/',
    #         'https://familydoctor.ru/prices/hirurgicheskaya-stomatologiya/',
    #         'https://familydoctor.ru/prices/child/hirurgicheskaya-stomatologiya/'
    #     ],
    #     'process': familydoctor
    # },
    # 'https://nydc.ru/uslugi-i-tseny/': {
    #     'links': ['https://nydc.ru/uslugi-i-tseny/'],
    #     'process': nydc
    # },
    # 'https://www.orthodont-elit.ru/price/': {
    #     'links': ['https://www.orthodont-elit.ru/price/full/'],
    #     'process': orthodont
    # },
    # 'https://www.alfa-clinic.ru': {
    #     'links': ['https://www.alfa-clinic.ru/czenyi/'],
    #     'process': alfaclinic
    # },
    # 'https://www.dentalfantasy.ru': {
    #     'links': ['https://www.dentalfantasy.ru/price-list/'],
    #     'process': dentalfantasy
    # },
    # 'https://zub.ru': {
    #     'links': ['https://zub.ru/price-list/'],
    #     'process': zub_ru
    # },
    # 'https://www.prezi-dent.ru': {
    #     'links': ['https://www.prezi-dent.ru/frunzenskaya/uslugi-i-tseny'],
    #     'process': prezi_dent
    # },
    # 'https://mositaldent.ru': {
    #     'links': ['https://mositaldent.ru/tseny'],
    #     'process': mositaldent
    # },
    # 'https://generation.family': {
    #     'links': ['https://generation.family/division'],
    #     'process': generation_family
    # },
    # 'https://docdent.ru/': {
    #     'links': ['https://docdent.ru/tseny/'],
    #     'process': docdent
    # },
    # 'https://alfazdrav.ru': {
    #     'links': ['https://alfazdrav.ru/services/price/'],
    #     'process': alfazdrav
    # },
    # 'https://lcenter.ru': {
    #     'links': ['https://lcenter.ru/directions/stomatologiya#price'],
    #     'process': lcenter
    # },
    # 'https://slavdent.ru': {
    #     'links': ['https://slavdent.ru/prices/'],
    #     'process': slavdent
    # },
    # 'https://artdent.ru': {
    #     'links': [
    #         'https://artdent.ru/cena2.html',
    #         'https://artdent.ru/cenaprotes.html',
    #         'https://artdent.ru/surgery.html',
    #         'https://artdent.ru/implantology.html',
    #         'https://artdent.ru/cenaparodont.html',
    #         'https://artdent.ru/ortodonty.html',
    #     ],
    #     'process': artdent
    # },
    # 'https://www.drelmar.ru': {
    #     'links': ['https://www.drelmar.ru/price'],
    #     'process': drelmar
    # },
    'https://evklaz-clinik.ru/prajslist': {
        'links': ['https://evklaz-clinik.ru/prajslist'],
        'process': evklaz
    }
}


async def work():
    with open('stomatolog_msk_1/url_list.txt', 'r') as file:
        urls = [i.strip() for i in file.readlines()]
    for url in urls:
        site = dependencies.get(url)
        if site:
            await site.get('process')(links=site.get('links'))
