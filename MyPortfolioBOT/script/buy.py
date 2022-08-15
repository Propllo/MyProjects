import requests
from bs4 import BeautifulSoup

HEADS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'
}


def Pars_Gecko(name_coin: str) -> list or False:
    """Функция осуществляющая поиск указанного токена пользователем

    name_coin - название токена (str)
    info_coin - список найденной информации о токене (list)
    url - ссылка на страницу сайта (str)
    data - изъятый набор информации со страницы сайта (list)
    price_coin - цена токена на данный момент (float)
    :returns False - если токен не найден или info_coin - информацию о токене"""
    info_coin = []
    url = f"https://www.coingecko.com/en/coins/{name_coin.lower().strip().replace(' ', '-')}"
    response = requests.get(url, HEADS)
    soup = BeautifulSoup(response.text, 'lxml')
    data = soup.find_all('div', class_="tw-col-span-2 md:tw-col-span-2")
    if len(data) == 0:
        return False
    for i in data:
        name_coin = i.find('div', class_="mr-md-3 tw-pl-2 md:tw-mb-0 tw-text-xl tw-font-bold tw-mb-0").text.replace(
            '\n', '')
        price_coin = i.find('span', class_="no-wrap").text.replace('\n', '')
        price_coin = price_coin.replace('$', '')
        price_coin = price_coin.replace(',', '')
        info_coin.append(name_coin)
        info_coin.append(float(price_coin))
    return info_coin



