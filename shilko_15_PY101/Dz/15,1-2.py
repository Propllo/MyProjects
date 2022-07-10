import json


def create_json(name: str):
    """Функция создающая документ .json с покупками и ценами

    name - имя создаваемого файла (str)
    goods - товар (str)
    price - цена (int)
    :return название файла
    """
    with open(f'{name}.json', 'w', encoding='UTF-8') as f:
        goods: str
        price: int
        di = {}
        while True:
            goods = input('Введите товар: ').lower().rstrip().title()
            if goods == 'Stop' or goods == 'Стоп':
                break
            price = int(input(f'Цена товара {goods}: '))
            di.update({goods: price})
        json.dump(di, f)
    return name


def read(name: str):
    """Функция выводящая сумму покупок из документа

    di - список цены товаров (lst)
    :return сумма покупок"""
    with open(f'{name}.json', encoding='UTF-8') as f:
        di = dict(json.load(f)).values()
        return f'Сумма покупок: {sum(di)}'


print(read(create_json('Введите название создаваемого файла: ')))
