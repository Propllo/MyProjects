"""Второй вариант логичный, но не красивый..."""

class Tomato:
    """Класс создающий плод

    states - стадии состояния (list)
    _state - начальная стадия (str)
    _index - номер плода (int)
    """
    states = ['Зарождение', 'Рост', 'Зрелость']

    def __init__(self, index):
        self._index = index
        self._state = Tomato.states[0]

    def grow(self):
        """Метод повышающий зрелость плода
        """
        if self._state == Tomato.states[0]:
            self._state = Tomato.states[1]
        elif self._state == Tomato.states[1]:
            self._state = Tomato.states[2]
        else:
            self._state = Tomato.states[2]

    def is_ripe(self):
        """Метод проверяющий зрелость плода
        """
        if self._state == Tomato.states[2]:
            return True
        else:
            return False


class TomatoBush:
    """Класс в котором создается куст томата

    count - кол-во томатов в кусте (int)
    tomatos - список томатов в кусте (dict)
    """

    def __init__(self, count):
        self.tomatos = [Tomato(_) for _ in range(count)]

    def grow_all(self):
        """Метод повышающий зрелость всех томатов
        """
        for tomato in self.tomatos:
            tomato.grow()

    def all_are_ripe(self):
        """Метод проверяющий все томаты на зрелость

        :return True or False
        """
        for tomato in self.tomatos:
            if not tomato.is_ripe():
                return False
        return True

    def give_away_all(self):
        """Метод очищающий список томатов
        """
        self.tomatos.clear()


class Gardener:
    """Класс работяги

    name - имя (str)
    _plant - ссылка на куст (_dict)
    """

    def __init__(self, name):
        self.name = name
        self._plant = TomatoBush(5)

    def work(self):
        """Метод повышающий зрелость
        """
        self._plant.grow_all()
        print('Все томаты на кусту подросли')

    def harvest(self):
        """Метод проверяющий зрелость всех томатов и если они все зрелые очищает список
        """
        if self._plant.all_are_ripe():
            print('Все томаты созрели проводим сбор')
            return self._plant.give_away_all()
        else:
            print('Не все томаты созрели')


def run():
    gard = Gardener('Aabobus')
    gard.work()
    gard.harvest()
    gard.work()
    gard.harvest()


run()
