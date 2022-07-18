class TomatoBash:
    """Класс в котором создаются томаты
    count - кол-во томатов (int)
    tomatos - словарь томатов (dict)
    """
    tomatos = {}

    def __init__(self, count):
        self.count = count

    def create_to(self):
        """Метод создающий словарь томатов
        """
        for i in range(1, self.count + 1):
            self.tomatos.update({f'Tomato {i}': {'Индекс зрелости': 1,
                                                 'Зрелость': False}})

    def grow_all(self):
        """Метод повышающий индекс зрелости всех томатов на 1
        """
        for i in range(1, len(self.tomatos) + 1):
            if self.tomatos[f'Tomato {i}']['Индекс зрелости'] == 1:
                self.tomatos[f'Tomato {i}']['Индекс зрелости'] = 2
                continue
            else:
                self.tomatos[f'Tomato {i}']['Индекс зрелости'] = 3
                self.tomatos[f'Tomato {i}']['Зрелость'] = True

    def give_away_all(self):
        """Метод очищающий словарь томатов
        """
        self.tomatos.clear()

    def all_are_ripe(self):
        """Метод проверяющий все томаты на зрелость

        :return True or False
        """
        count2 = 0
        for i in range(1, len(self.tomatos) + 1):
            if self.tomatos[f'Tomato {i}']['Зрелость']:
                count2 += 1
        if count2 == len(self.tomatos):
            return True
        else:
            return False


class Tomato:
    """Класс содержащий некоторые методы действия над томатами
    """
    states = [1, 2, 3]

    def __init__(self, index):
        self._index = index

    def grow(self):
        """Метод повышающий выбранный томат на 1
        """
        try:
            TomatoBash.tomatos[f'Tomato {self._index}']['Индекс зрелости'] += 1
        except KeyError:
            print('Такого томата у вас нету')
        else:
            if TomatoBash.tomatos[f'Tomato {self._index}']['Индекс зрелости'] == 4:
                TomatoBash.tomatos[f'Tomato {self._index}']['Индекс зрелости'] = 3
            if TomatoBash.tomatos[f'Tomato {self._index}']['Индекс зрелости'] == 3:
                TomatoBash.tomatos[f'Tomato {self._index}']['Зрелость'] = True

    def is_ripe(self):
        """Метод проверяющий выбранный томат на зрелость
        """
        try:
            if TomatoBash.tomatos[f'Tomato {self._index}']['Зрелость']:
                print(f'Tomato {self._index} созрел')
            else:
                print(f'Tomato {self._index} не созрел')
        except KeyError:
            print('Такого томата нету')


class Gardener:
    """Класс игрока который отвечает за его действия

    name - имя игрока (str)
    _plant - ссылка на томаты (_dict)
    """
    income = 0

    def __init__(self, name):
        self.name = name
        self._plant = TomatoBash.tomatos

    def work(self):
        """Метод повышающий индекс зрелости на 1
        """
        choice = Tomato(int(input('Выберите номер Tomato: ')))
        choice.grow()

    def is_ripe_n(self):
        """Метод проверяющий зрелость
        """
        choice = Tomato(int(input('Выберите номер Tomato: ')))
        choice.is_ripe()

    def harvest(self):
        """Метод проверяющий зрелость всех томатов и если они все зрелые очищает словарь"""
        count2 = 0
        for i in range(1, len(self._plant) + 1):
            if self._plant[f'Tomato {i}']['Зрелость']:
                count2 += 1
        if count2 == len(self._plant):
            print('Все томаты созрели и были собраны')
            self.income += len(self._plant)
            self._plant.clear()

        else:
            print('Не все томаты созрели')

    @staticmethod
    def knowledge_base():
        """Статик метод показывающий информацию о методах данной программы"""
        print(f'Функции игрока: \n'
              f'1. work - ухаживание за определенным томатом; \n'
              f'2. is_ripe_n - проверка опредленного томата на зрелость; \n'
              f'3. harvest - проверка всех томатов на зрелость и в случаи если они все созрели собирает все; \n'
              f'Функции админа для обьекта класса TomatoBash: \n'
              f'1. grow_all - поднять индекс зрелости на 1 всем томатам; \n'
              f'2. give_away_all - очистить словарь томатов; \n'
              f'3. is_ripe - проверка всех томатов на зрелость; \n')


def run(name: str, count_to: int):
    """Функция отыгрыша сценария
    """
    tomatos = TomatoBash(count_to)
    tomatos.create_to()
    gard = Gardener('Aby')
    print('Ваш огород:')
    print(gard._plant)
    gard.knowledge_base()
    while True:
        ch = int(input(f'Выберите действие: \n'
                       f'1. Ухаживание за определенным томатом;\n'
                       f'2. Проверка опредленного томата на зрелость;\n'
                       f'3. проверка всех томатов на зрелость и в случаи если они все созрели собирает все;\n'))
        if ch == 1:
            gard.work()
            print(gard._plant)
        elif ch == 2:
            gard.is_ripe_n()
            print(gard._plant)
        elif ch == 3:
            gard.harvest()
        else:
            print('Такого действия нету')
        if len(gard._plant) == 0:
            break
    print('Сезон завершен')


while True:
    run(input('Введите имя персонажа: '), int(input('Введиет кол-во томатов которые будут посажены: ')))
    ch = input('Заново? (+/-): ').rstrip()
    if ch == '+':
        continue
    else:
        break
