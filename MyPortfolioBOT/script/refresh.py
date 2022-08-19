import sqlite3
from script import buy


def refresh(id: int):
    """Функция обновляющая ценность токенов в БД

    id - id пользователя (int)
    """
    def update_db(name: str, price: float):
        """Функция обновляющая БД

        name - название токена (str)
        price - цена токена на данный момент (float)
        count - кол-во токенов у пользователя (float)
        """
        cursor.execute(f"SELECT Count FROM id_{id} WHERE Name_Token = (?)", (name,))
        count = cursor.fetchall()[0][0]
        cursor.execute(f"UPDATE id_{id} SET Price = (?) WHERE Name_Token = (?)", (price, name))
        conn.commit()
        cursor.execute(f"UPDATE id_{id} SET Total = (?) WHERE Name_Token = (?)", (price * count, name))
        conn.commit()

    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()

    try:
        cursor.execute(f"SELECT Name_Token FROM id_{id}")
        lst_name = cursor.fetchall()
    except:
        text = 'Пока нечего обновлять'
        return text
    else:
        if len(lst_name) > 0:
            for name_i in lst_name:
                name_i = name_i[0]
                name_i = name_i[:name_i.find('(')]
                lst_info = buy.Pars_Gecko(name_i)
                if isinstance(lst_info, list):
                    name_i = lst_info[0]
                    price = lst_info[1]
                    update_db(name_i, price)
                else:
                    continue
            text = 'Обновлено'
            return text
        else:
            text = 'Пока нечего обновлять'
            return text





