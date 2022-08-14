import sqlite3

di = {'token': 'Bitcoin (BTC)', 'price': 24456.71, 'choice': 1, 'count': 100.0, 'mark': 'MM'}


def save_data(id: int, dict_info: dict = None):
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()

    cursor.execute(f'''CREATE TABLE IF NOT EXISTS
                        id_{id}(
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        Name_Token TEXT,
                        Prise REAL,
                        Count REAL,
                        Note TEXT,
                        Total REAL
                        )
                        ''')
    cursor.execute(f'''INSERT INTO id_{id}(Name_Token, Prise, Count, Note, Total) VALUES (?, ?, ?, ?, ?)''',
                   (dict_info['token'], dict_info['price'], dict_info['count'], dict_info['mark'],
                    dict_info['price'] * dict_info['count']))
    conn.commit()
    cursor.execute(f'SELECT * FROM id_{id}')
    conn.commit()
    print(cursor.fetchall())


save_data(1, di)
