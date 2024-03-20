async def work():
    with open('stomatolog_msk_1/url_list.txt', 'r') as file:
        urls = [i.strip() for i in file.readlines()]
