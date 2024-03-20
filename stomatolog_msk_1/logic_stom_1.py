import asyncio

from bs4 import BeautifulSoup

from func import get_html


async def martirosyan_pro(links: list):
    result_dict = dict()
    result_dict['company'] = 'Клиника Артура Мартиросяна'
    result_dict['address'] = 'Большой Саввинский переулок дом 12с6'
    result_dict['site'] = 'https://martirosyan.pro/'
    # result_dict['category'] =
    for url in links[:1]:
        html = await get_html(url)
        soup = BeautifulSoup(markup=html, features='lxml')
        parents = soup.find_all(name='div', attrs={'class': 't849__wrapper'})
        for parent in parents:
            print('\n', parent.find_next(name='span', attrs={'class': 't849__title t-name t-name_xl'}).getText())
            childs = parent.findChildren('li')
            for c in childs:
                print('--', c.getText())


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
    }
}


async def work():
    with open('stomatolog_msk_1/url_list.txt', 'r') as file:
        urls = [i.strip() for i in file.readlines()]
    for url in urls:
        site = dependencies.get(url)
        if site:
            await site.get('process')(links=site.get('links'))
