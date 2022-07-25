def card():
    """Функция перебора карт из колоды

    num - список значений карт (list)
    m - список мастей карт (list)
    num_i - индекс позиции значения в num (int)
    m - индекс позиции значения в m (int)

    :return карта из колоды (str)
    """
    num = [2, 3, 4, 5, 6, 7, 8, 9, 10, 'B', 'D', 'K', 'A']
    m = ['Пик', 'Черва', 'Бубна', 'Трефа']
    num_i = 0
    m_i = 0
    while True:
        if num_i >= len(num):
            num_i = 0
            m_i += 1
        if m_i == 4:
            raise StopIteration
        card_i = f'{num[num_i]} {m[m_i]}'
        num_i += 1
        yield card_i


def run():
    fi = card()
    while True:
        print(next(fi))


run()
