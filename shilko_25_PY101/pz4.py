import sqlite3

conn = sqlite3.connect('pz4.db')
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS 
                    tab_1(
                    id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    val INTEGER
                    )''')


class FormatData:

    def check_obj(self, val_1=None, val_2=None, val_3=None):
        """Метод класса, обрабатывающий попытку записи в БД по заданию
        """
        if val_1 is not None and val_2 is None and val_3 is None:
            cursor.execute(f"INSERT INTO tab_1(val) VALUES (3)")
            conn.commit()

        if val_1 is not None and val_2 is not None and val_3 is None:
            if isinstance(val_2, int):
                cursor.execute(f"DELETE FROM tab_1 WHERE id=1")
                conn.cursor()

        if val_1 is not None and val_2 is not None and val_3 is not None:
            if isinstance(val_3, int):
                cursor.execute(f"UPDATE tab_1 SET val=77 WHERE id=3")
                conn.commit()


obj = FormatData()
obj.check_obj(1)
obj.check_obj(1, '1', 3)
obj.check_obj(1, 1)

cursor.execute("SELECT*FROM tab_1")
print(cursor.fetchall())
