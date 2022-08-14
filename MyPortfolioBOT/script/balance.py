import json


def balance():
    with open('D:\Projects PYTHON\MyPortfolioBOT\DATA\data.json', 'r') as file:
        read = dict(json.load(file))
    sum_balance = 0
    keys = read.keys()
    if len(read.items()) == 0:
        return sum_balance
    else:
        for key in keys:
            value = read[key]['USD']
            sum_balance += value
        return sum_balance


def my_portfolio():
    info = ''
    with open('D:\Projects PYTHON\MyPortfolioBOT\DATA\data.json', 'r') as file:
        read = dict(json.load(file))
    if len(read.items()) == 0:
        return ''
    else:
        for key in read.keys():
            info += f"{key}: Кол-во токенов {read[key]['TOKENS']}: Cумма в USD {read[key]['USD']}\n"
        return info


