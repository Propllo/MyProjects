import sqlite3
from script import buy

id = 390226986
name = 'Bitcoin (BTC)'


def dict_token(id_user: int) -> dict or False:
    conn = sqlite3.connect('D:\Projects PYTHON\MyPortfolioBOT\data.db')
    cursor = conn.cursor()

    dict_name = {}
    i = 1
    cursor.execute(f"SELECT Name_Token FROM id_{id_user}")
    list_name = cursor.fetchall()
    for string in list_name:
        dict_name.update({i: string[0]})
        i += 1
    if len(dict_name) > 0:
        return dict_name
    else:
        return False



