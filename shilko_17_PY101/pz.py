class Human:
    def_age = 1
    def_name = 'abab'

    def __init__(self, name=def_name, age: int = def_age, money: int = 0):
        self.name = name
        self.age = age
        self.__money = money
        self.__house = 'box'

    def info(self):
        print([self.name, self.age, self.__money, self.__house])

    def earn_money(self):
        self.__money += 100

    def make_dial(self):
        self.__money = self.__money - house._price
        self.__house = House.name
        print(self.__money)

    def buy_house(self):
        print(f'Дом: {House.name}')
        print(f'Скидка: {house.discount}')
        a = self.__money - house.final_price()
        return a

    @staticmethod
    def def_info():
        print(Human.def_name, Human.def_age)


class House:
    name = 'House'
    _area = 100
    _price = 100000
    discount_k = 0.1
    discount = 0

    def __init__(self, area=_area, price=_price):
        self._area = area
        self._price = price
        self.discount = self._price * self.discount_k

    def final_price(self):
        self._price = self._price - self.discount
        return self._price


class SmallHouse(House):
    def __init__(self, _area=40, _price=50000):
        super().__init__(_area, _price)


chel = Human(input('Введите имя: '), int(input('Возраст: ')), int(input('Кол-во денег: ')))
print('До: ')
chel.info()
h_s = int(input('Выберите дом: 1. Обычный; 2. Маленький: '))
if h_s == 1:
    house = House()
    if chel.buy_house() < 0:
        print('Недостаточно денег')
    else:
        chel.make_dial()
        print('После: ')
        chel.info()
elif h_s == 2:
    house = SmallHouse()
    if chel.buy_house() < 0:
        print('Недостаточно денег')
    else:
        chel.make_dial()
        print('После: ')
        chel.info()
else:
    print('Такого нету')




