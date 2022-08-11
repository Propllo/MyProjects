import sqlite3
import random

conn = sqlite3.connect('pz5.db')
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS 
                    tab_1(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    text_1 TEXT,
                    text_2 TEXT
                    )''')


def insert_3():
    """Функция генерирующая 3 случайные записи и записывающая их в БД
    """
    for i in range(3):
        text_1 = str(random.randint(0, 1000))
        text_2 = str(random.randint(0, 1000))
        cursor.execute(f"INSERT INTO tab_1(text_1, text_2) VALUES ({text_1}, {text_2})")
        conn.commit()
    cursor.execute('''SELECT*FROM tab_1''')
    print(cursor.fetchall())


def delete_id2():
    """Функция удаляющая вторую запись из БД
    """
    cursor.execute("DELETE FROM tab_1 WHERE id=2")
    conn.commit()
    cursor.execute('''SELECT*FROM tab_1''')
    print(cursor.fetchall())


def update_id3():
    """Функция обновляющая третью запись в БД по заданию
    """
    cursor.execute("UPDATE tab_1 SET text_1='hello' WHERE id=3")
    conn.commit()
    cursor.execute("UPDATE tab_1 SET text_2='world' WHERE id=3")
    conn.commit()
    cursor.execute('''SELECT*FROM tab_1''')
    print(cursor.fetchall())


def text() -> str:
    """Функция считывающая БД и переводящая все в текст
    :return text(str)
    """
    data = list(cursor.execute("SELECT*FROM tab_1"))
    text = 'id\ttext_1\ttext_2\n'
    lst_text = []
    for i in data:
        for j in i:
            lst_text.append(str(j))
        text += f"{lst_text[0]}\t{lst_text[1]}\t\t{lst_text[2]}\n"
        lst_text.clear()
    return text


def save_text(text: str):
    """Функция сохраняющая полученный текст в txt файл
    """
    with open('pz5.txt', 'w+') as file:
        file.write(text)


def run():
    insert_3()
    delete_id2()
    update_id3()
    t = text()
    save_text(t)


run()
