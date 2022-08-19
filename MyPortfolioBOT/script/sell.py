import sqlite3


def dict_token(id_user: int) -> dict or str:
    """Функция получающая словарь имен токенов в БД

    id_user - id пользователя (int)
    dict_name - словарь имен (dict)
    list_name - список имен (list)

    :returns строку или словарь имен в зависимости от наличия имен
    """
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()

    dict_name = {}
    i = 1
    try:
        cursor.execute(f"SELECT Name_Token FROM id_{id_user}")
        list_name = cursor.fetchall()
    except:
        text = 'У вас нету ничего для изменения.'
        return text
    else:
        if len(list_name) > 0:
            for string in list_name:
                dict_name.update({i: string[0]})
                i += 1
            return dict_name
        else:
            text = 'У вас нету ничего для изменения.'
            return text

