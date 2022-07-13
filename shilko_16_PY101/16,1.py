class StrOrInt:
    def __init__(self, a: str):
        self.a = a.strip().lower()
        if a.isdigit():
            self.a = int(self.a)

    def pod1(self):
        """Метод обрабатывающий строку или число по заданию 1
        """
        def st(a: str):
            """Функция метода обрабатывающая строку

            lst - список гласных символов (lst)
            su_vo - сумма гласных (int)
            cons - сумма согласных (int)
            :return набор символов согласных или гласных букв
            """
            lst = ['a', 'e', 'i', 'o', 'u', 'y']
            su_vo = 0
            for i in lst:
                su_vo += a.count(i)
            cons = len(a) - su_vo
            if su_vo / cons >= len(a):  # если частное деления гласных на согласные больше либо равна длины, то строка
                # гласных
                lst2 = []
                for i in lst:
                    if a.count(i) > 0:
                        lst2.append(f'{i} ' * a.count(i))
                        lst2 = ' '.join(lst2)
                        print(lst2)
                    else:
                        continue
            else:   # иначе строка согласных букв
                lst2 = []
                for i in a:
                    lst2.append(i)
                for i in range(len(lst2) - 1, -1, -1):
                    for j in lst:
                        if lst2[i] == j:
                            del lst2[i]
                            break
                print(' '.join(lst2))

        def inta(a: int):
            """Функция метода обрабатывающая число

            lst - список четных значений
            :return произведение суммы четных чисел на длину исходного числа"""
            a = str(a)
            count = len(a)
            lst = [int(_) for _ in a if int(_) % 2 == 0]
            return sum(lst) * count

        if isinstance(self.a, str):
            st(self.a)
        else:
            print(inta(self.a))

    def pod2(self):
        """Метод выдающий длину числа или строки

        :return длина строки или числа"""
        if isinstance(self.a, int):
            self.a = str(self.a)
            return len(self.a)
        else:
            return len(self.a)


def run():
    a = StrOrInt(input('Введите число или слово: '))
    a.pod1()
    print(a.pod2())


run()
