import requests
from bs4 import BeautifulSoup
from time import sleep
import csv
import json


def sort_u(di: dict):
    """Функция сортирующая словарь функции pars_di() по usd

    di - словарь с данными о BMV E60 (dict)
    di2 - упрощенный словарь по ключу и цене в USD (dict)
    :return отсортированный словарь по USD (min-max) (dict)
    """
    di2 = {}
    di3 = {}
    for i in range(1, len(di) + 1):  # проносимся по заранее ведомым ключам
        di2.update({i: di[i]['Цена в USD']})  # получаем упрощенный словарь с ключами и их привязкой к USD
    di2_keys = sorted(di2, key=di2.get)  # словарь по значению ключей и получаем список упорядоченных ключей по цене
    for i in di2_keys:  # проносимся по значениям в списке и восстанавливаем словарь по новому рассположению ключей
        di3.update({i: di[i]})
    di2.clear()
    return di3


def text_csv(di: dict):
    """Функция записывающая словарь в документ csv

    di - словарь (dict)
    """
    with open('BMV E60.csv', 'w+', encoding='UTF-8', newline='') as f:
        file = csv.writer(f, delimiter=':')
        lst = []
        for i in di.items():
            lst.append(i)
        for line in lst:
            file.writerow(line)


def text_json(di: dict):
    """Функция записывающая словарь в документ json

    di - словарь (dict)
    """
    # функция почему-то не совсем корректно работает так как в документе словарь не запиcывается как по PEP поэтому
    # в документе нежно нажать сразу (CTRL + ALT + L).
    with open('BMV.json', 'w+', encoding='UTF-8') as f:
        json.dump(di, f, ensure_ascii=False)


def pars_di():
    """Функция парсит сайт av.by на инфу по BMV E60

    page - переменная страницы сайта (int)
    count - счетчик для ключей списка (int)
    di_av - словарь для заполнения инфы (dict)
    :return словарь со всеми обьявлениями BMV E60
    """
    # немного упрощено ввиду того, что мы знаем что мы ищем (E60) поэтому фильтруем непосредственно
    # на сайте (BMV серия 5)
    page = 0
    count = 0
    di_av = {}
    while True:
        sleep(3)  # увеличиваем промежуток время запросов от нас к сайту (иначе могут забанить)
        url = f"https://cars.av.by/filter?brands[0][brand]=8&brands[0][model]=5865&page={page}"  # ссылка на
        # страницу (серии 5). Чтобы проверить быстро на работоспособность вместо page поставьте '1'
        # и убрать break в конце цикла
        response = requests.get(url)  # получаем ответ от сайта
        soup = BeautifulSoup(response.text, 'lxml')  # обрабатываем код html страницы; 'lxml'- анализатор html кода
        data = soup.find_all('div', class_='listing-item')  # записываем все обьявления на сайте в список
        if len(data) == 0:
            break
        for i in data:  # вытаскиваем по обьявлению
            name = i.find('h3', class_='listing-item__title').text.replace('\n', '')    # выделяем интересующую нас
            # информацию и убираем траблы
            if name != 'BMW 5 серия E60, E61':
                continue
            print(name)
            count += 1
            price_rub = i.find('div', class_='listing-item__price').text.replace('\xa0', '')
            price_rub = price_rub.replace('\u2009', '')
            price_rub = price_rub.replace('р.', '')
            price_usd = i.find('div', class_='listing-item__priceusd').text.replace(chr(8776), '')
            price_usd = price_usd.replace('\xa0', '')
            price_usd = price_usd.replace('\u2009', '')
            price_usd = price_usd.replace('$', '')
            link = 'https://cars.av.by' + i.find('a', class_='listing-item__link').get("href")
            print(link)
            info = i.find('div', class_='listing-item__params').text.replace('\xa0', ' ')
            info = info.replace('\u2009', '')
            di = {count: {'Cсылка': link, 'Цена в USD': int(price_usd), 'Цена в BYN': int(price_rub), 'Инфа': info}}
            di_av.update(di)    # и закидываем все в словарь
            page += 1
            # break  # если проверять работоспособность на одну страницу
    return di_av


def run():
    """Функция запускающая сценарий
    """
    sort_usd = sort_u(pars_di())
    text_csv(sort_usd)
    text_json(sort_usd)


run()