import sqlite3


def check_db(id_user: int) -> str:
    """Функция обработки информации в БД

    id_user - id пользователя (int)
    :return информацию о токенах, если такая есть
    """
    def create_info(data_t: list) -> str:
        """Функция перевода информации из БД в строку

        data_t - информация о токене из БД (list)
        info - информация о токене (str)
        :return информацию о токене (str)"""
        info = ''
        for string_db in data:
            lst_info = []
            for i in range(len(string_db)):
                lst_info.append(string_db[i])
            info += f'{lst_info[0]} - Кол-во: {round(lst_info[1], 2)} - Цена: {round(lst_info[3], 2)}$ ' \
                    f'- Заметка: {lst_info[2]}\n'
        return info

    conn = sqlite3.connect('D:\Projects PYTHON\MyPortfolioBOT\data.db')
    cursor = conn.cursor()

    try:
        cursor.execute(f"SELECT Name_Token, Count, Note, Total FROM id_{id_user}")
    except sqlite3.OperationalError:
        return 'Вы пока ничего не добавили'

    data = cursor.fetchall()

    if len(data) == 0:
        return 'Пока здесь ничего нету'
    else:
        return create_info(data)


def total_money(id_user: int) -> int:
    """Функция подсчитывающая ценность портфеля

    id_user - id пользователя (int)
    total - ценность портфеля (float)
    :return ценность портфеля (float)
    """
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()

    total = 0
    try:
        cursor.execute(f"SELECT Total FROM id_{id_user}")
    except sqlite3.OperationalError:
        return 0

    data = cursor.fetchall()
    if len(data) != 0:
        for string_db in data:
            total += string_db[0]
        return round(total, 2)
    else:
        return 0




