import sqlite3

conn1 = sqlite3.connect('dz_tabl_1.db')
cursor1 = conn1.cursor()
conn2 = sqlite3.connect('dz_tabl_2.db')
cursor2 = conn2.cursor()

cursor1.execute('''CREATE TABLE IF NOT EXISTS 
                    tab_1(
                    id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    text TEXT
                    )''')
cursor2.execute('''CREATE TABLE IF NOT EXISTS 
                    tab_1(
                    id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    dig INTEGER
                    )''')

lst = ['pts', 1000, 'low', 'priest', 'topcheg', 300, 'bucks?', 'ok', 'lets', 'go', 666, 1]


def check_list(lst: list):
    """Функция обрабатывающая список и вносящая изменения в БД по заданию
    """
    def text(word: str):
        """Функция обработки строки по заданию
        """
        cursor1.execute('''INSERT INTO tab_1(text) VALUES (?)''', (word,))
        conn1.commit()
        cursor2.execute('''INSERT INTO tab_1(dig) VALUES (?)''', (int(len(word)),))
        conn2.commit()

    def number(num: int):
        """Функция обработки числа по заданию
        """
        if num % 2 == 0:
            cursor2.execute(f"INSERT INTO tab_1(dig) VALUES ({num})")
            conn2.commit()
        else:
            cursor1.execute(f"INSERT INTO tab_1(text) VALUES ('Нечетное')")
            conn1.commit()

    def more_less():
        """Функция обработки условия для второй базы данных по заданию
        """
        data_dig_len = len(list(cursor2.execute("SELECT*FROM tab_1")))
        if data_dig_len > 5:
            cursor1.execute("DELETE FROM tab_1 WHERE id=1")
            conn1.commit()
        elif data_dig_len < 5:
            cursor1.execute("UPDATE tab_1 SET dig='hello' WHERE id=1")
            conn1.commit()

    for i in lst:
        if isinstance(i, str):
            text(i)
        elif isinstance(i, int):
            number(i)
    more_less()


def run():
    check_list(lst)
    cursor1.execute("SELECT*FROM tab_1")
    cursor2.execute("SELECT*FROM tab_1")
    print(cursor1.fetchall())
    print(cursor2.fetchall())


run()
