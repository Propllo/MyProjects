import sqlite3


def save_data(id: int, dict_info: dict):
    """Функция сохраняющая и обновляющая полученную информацию в базу данных

    id - id пользователя (int)
    dict_info - полученная информация о токене (dict)
    """

    def token():
        """Функция добавляющая в БД информацию о токене если его нету в БД при условии, что пользователь выбрал
        добавление в токенах
        """
        cursor.execute(f'''INSERT INTO id_{id}(Name_Token, Price, Count, Note, Total) VALUES (?, ?, ?, ?, ?)''',
                       (dict_info['token'], dict_info['price'], dict_info['count'], dict_info['mark'],
                        dict_info['price'] * dict_info['count']))
        conn.commit()

    def dollar():
        """Функция добавляющая в БД информацию о токене если его нету в БД при условии, что пользователь выбрал
            добавление в долларах
            """
        count_dollar = dict_info['count']
        count_token = count_dollar / dict_info['price']
        cursor.execute(f'''INSERT INTO id_{id}(Name_Token, Price, Count, Note, Total) VALUES (?, ?, ?, ?, ?)''',
                       (dict_info['token'], dict_info['price'], count_token, dict_info['mark'],
                        count_dollar))
        conn.commit()

    def availability(name_token: str = dict_info['token']) -> True or False:
        """Функция проверяющая есть ли указанный токен в БД

        name_token - название токена (str)
        dict_info - dict_info - полученная информация о токене (dict)
        true - проверка на содержание (int)
        """
        cursor.execute(f'''SELECT Name_Token FROM id_{id} WHERE Name_Token = ?''', (name_token,))
        true = len(cursor.fetchall())

        if true == 1:
            return True
        else:
            return False

    def update_token():
        """Функция обновляющая изменяющая информацию о токене, если такой есть в БД и учитывающая выбор
        пополнения пользователя в токенах.

        old_count_token - кол-во токенов до изменения (float)
        count_token - кол-во токенов которое получается после изменения (float)
        """
        cursor.execute(f"SELECT Count FROM id_{id} WHERE Name_Token = (?)", (dict_info['token'],))
        old_count_token = cursor.fetchall()[0][0]
        count_token = dict_info['count'] + old_count_token
        cursor.execute(f"UPDATE id_{id} SET Price = {dict_info['price']} WHERE Name_Token = (?)", (dict_info['token'],))
        conn.commit()
        cursor.execute(f"UPDATE id_{id} SET Count = {count_token} WHERE Name_Token = (?)", (dict_info['token'],))
        conn.commit()
        cursor.execute(f"UPDATE id_{id} SET Note = (?) WHERE Name_Token = (?)", (dict_info['mark'], dict_info['token']))
        conn.commit()
        cursor.execute(f"UPDATE id_{id} SET Total = {dict_info['price'] * count_token} WHERE Name_Token = (?)",
                       (dict_info['token'],))
        conn.commit()

    def update_dollar():
        """Функция обновляющая изменяющая информацию о токене, если такой есть в БД и учитывающая выбор
        пополнения пользователя в долларах.

        old_count_t - кол-во токенов до изменения (float)
        count_token - кол-во токенов которое получается после изменения (float)
        """
        cursor.execute(f"SELECT Count FROM id_{id} WHERE Name_Token = (?)", (dict_info['token'],))
        old_count_t = cursor.fetchall()[0][0]
        count_token = dict_info['count'] / dict_info['price'] + old_count_t
        cursor.execute(f"UPDATE id_{id} SET Price = {dict_info['price']} WHERE Name_Token = (?)", (dict_info['token'],))
        conn.commit()
        cursor.execute(f"UPDATE id_{id} SET Count = {count_token} WHERE Name_Token = (?)", (dict_info['token'],))
        conn.commit()
        cursor.execute(f"UPDATE id_{id} SET Note = (?) WHERE Name_Token = (?)", (dict_info['mark'], dict_info['token']))
        conn.commit()
        cursor.execute(f"UPDATE id_{id} SET Total = {dict_info['price'] * count_token} WHERE Name_Token = (?)",
                       (dict_info['token'],))
        conn.commit()

    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()

    cursor.execute(f'''CREATE TABLE IF NOT EXISTS
                        id_{id}(
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        Name_Token TEXT,
                        Price REAL,
                        Count REAL,
                        Note TEXT,
                        Total REAL
                        )
                        ''')

    if availability():
        if dict_info['choice'] == 1:
            update_token()
        else:
            update_dollar()
    else:
        if dict_info['choice'] == 1:
            token()
        else:
            dollar()


def data_sell(id: int, dict_info: dict):
    """Функция изменяющая баланс в портфеле или удаляющая его

    id - id пользователя (int)
    dict_info - полученная информация о токене (dict)
    """

    def token_sell():
        """Функция изменяющая баланс при выборе изменения в токенах

        old_count_token - старое кол-во токенов (float)
        new_count - кол-во токенов после изменения (float)
        """
        cursor.execute(f"SELECT Count FROM id_{id} WHERE Name_Token = (?)", (dict_info['token'],))
        old_count_token = cursor.fetchall()[0][0]
        new_count = old_count_token - dict_info['count']
        if new_count <= 0:
            cursor.execute(f"DELETE FROM id_{id} WHERE Name_Token = (?)", (dict_info['token'],))
            conn.commit()
        else:
            cursor.execute(f"UPDATE id_{id} SET Count = {new_count} WHERE Name_Token = (?)", (dict_info['token'],))
            conn.commit()
            cursor.execute(f"UPDATE id_{id} SET Price = {dict_info['price']} WHERE Name_Token = (?)",
                           (dict_info['token'],))
            conn.commit()
            cursor.execute(f"UPDATE id_{id} SET Total = {new_count * dict_info['price']} WHERE Name_Token = (?)",
                           (dict_info['token'],))
            conn.commit()

    def dollar_sell():
        """Функция изменяющая баланс при выборе изменения в долларах

        old_count_token - старое кол-во токенов (float)
        new_count - кол-во токенов после изменения (float)
        """
        cursor.execute(f"SELECT Count FROM id_{id} WHERE Name_Token = (?)", (dict_info['token'],))
        old_count_token = cursor.fetchall()[0][0]
        new_count = old_count_token - dict_info['count'] / dict_info['price']
        if new_count <= 0:
            cursor.execute(f"DELETE FROM id_{id} WHERE Name_Token = (?)", (dict_info['token'],))
            conn.commit()
        else:
            cursor.execute(f"UPDATE id_{id} SET Count = {new_count} WHERE Name_Token = (?)", (dict_info['token'],))
            conn.commit()
            cursor.execute(f"UPDATE id_{id} SET Price = {dict_info['price']} WHERE Name_Token = (?)",
                           (dict_info['token'],))
            conn.commit()
            cursor.execute(f"UPDATE id_{id} SET Total = {new_count * dict_info['price']} WHERE Name_Token = (?)",
                           (dict_info['token'],))
            conn.commit()

    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()

    if dict_info['choice'] == 1:
        token_sell()
    else:
        dollar_sell()
