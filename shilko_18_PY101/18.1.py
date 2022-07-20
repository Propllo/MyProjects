import os
import csv
import json
import re


def find_path(file_name: str):
    """Функция находящая путь файла в данной директории которая принимает название файла с расширением и без

    file_name - название файла (str)
    file1 - единица содержимого исходной директории (str)
    file2 - единица содержимого поддиректорий в директории (если они есть) (str)
    di - список содержимого исходной директории (lst)
    di2 - список содержимого поддиректории в директории (lst)
    :returns Путь к файлу если он есть или False если его нету
    """
    if os.path.exists(file_name):  # ищем наличие пути к файлу в исходной директории
        if not os.path.isdir:  # если это название директории скипаем
            return os.path.abspath(file_name)
    else:  # если нету, то проверяем список файлов на совпадение
        for file1 in os.listdir():
            if file1[:file1.find('.')] == file_name:  # данная проверка проводится если не было казано расширение
                if os.path.exists(file1):
                    return os.path.abspath(file1)
    for di in os.listdir():  # если ничего не нашло,то проносимся по списку в исходной директории и пытаемся
        # получить содержимое
        try:
            di2 = os.listdir(di)  # если это поддиректория, то проносимся по всех файлах в ней
        except NotADirectoryError:
            continue
        for file2 in di2:  # аналогично проносимся по поддиректории
            if file2[:file2.find('.')] == file_name:
                if os.path.exists(f'{di}/{file2}'):
                    return os.path.abspath(f'{di}/{file2}')
            elif file2 == file_name:
                if os.path.exists(f'{di}/{file2}'):
                    return os.path.abspath(f'{di}/{file2}')

    else:
        return False


def get_size(path: str):
    """Функция определяющая размер файла в байтах

    path - путь к файлу (str)
    :return размер файла (str)
    """
    if isinstance(path, str):
        size = os.path.getsize(path)
        return f'{size} байт'
    else:
        return False


def suf(path: str):
    """Функция определяющая расширение файла

    path - путь к файлу (str)
    :return расширение файла (str)
    """
    sufe = os.path.splitext(path)[-1]
    if sufe == '':
        sufe = '.txt'
    return sufe


def file_na(path: str):
    """Функция определяющая имя файла

    :return имя файла (str)"""
    name = os.path.basename(path)
    name = name[:name.find('.')]
    return name


def counter(fu):
    """Декоратор. Отвечает за наполнение словаря и проверку на дубликат
    """
    def email(s: str):
        """Функция декоратора вырезающая email если он есть

        s - информация из файла (str)
        :return список email-ов"""
        s = re.findall(r'\w+@\w+.\w+', s)
        print(f'Список найденных email-ов: {s}')

    def digits_3(s: str):
        """Функция декоратора, которая возвращает список чисел длинной в 3

        s - информация из файла (str)
        dig - список чисел (list)
        :return список чисел (lst)"""
        dig = re.findall('[0-9]{3,4}', s)
        lst = []
        for i in dig:   # список цифры которых от 3-х до 4-х значений и отсеиваем все что не с 3-мя
            if len(i) == 3:
                i = int(i)
                lst.append(i)
        print(f'Спаршеная информация из файле: {s}')
        print(f'Числа с тремя однозначными: {lst}')

    def read_str(x):
        """Функция декоратора, которая читает файлы и переводит их в строку с форматированием

        x - список информации о файле(list)
        :return строка спаршеной информации"""
        res = x
        if res[3] == '.csv':    # пробегаемся по расширениям и переводим все в одну строку
            with open(res[1], encoding='UTF-8') as file:
                reader = csv.reader(file)
                read_list = list(reader)
                reader = ''
                for i in read_list:
                    for j in i:
                        j = str(j)
                        j = j.replace('\n', '')
                        reader += f'{j} '
                return reader
        elif res[3] == '.json':
            with open(res[1], encoding='UTF-8') as file:
                reader = dict(json.load(file))
                reader_str = ''
                for i in reader.items():
                    for j in i:
                        j = str(j)
                        j = j.replace('\n', '')
                        reader_str += f'{j} '
                return reader_str
        else:
            with open(res[1], encoding='UTF-8') as file:
                reader = file.readlines()
                reader_str = ''
                for i in reader:
                    i = str(i).replace('\n', '')
                    reader_str += f'{i} '
                return reader_str

    def wrapper():
        """Функция обрабатывающая результат другой функции по заданиям"""
        nonlocal di
        res = fu()
        try:
            for i in di.keys():
                if res[0] == i:
                    res[0] = f'{res[0]}_Duplicate'
                    break
            di.update({res[0]: [res[1], res[2], res[3]]})
        except IndexError:
            print('Файла не существует')
        read = read_str(res)
        digits_3(read)
        email(read)
        return fu

    di = {}
    return wrapper


@counter
def information_gathering():
    """Функция собирает информацию по условию задания в список

    :return список спаршенной информации [имя, ссылка, размер, расширение] (dict)
    """
    lst_data = []
    path = find_path(input('Введите имя файла с расширением или без: '))
    try:
        lst_data.append(file_na(path))
        lst_data.append(path)
        lst_data.append(get_size(path))
        lst_data.append(suf(path))
    except TypeError:
        pass
    return lst_data


def run():
    """Функция отыгрывающая сценарий"""
    for _ in range(10):
        try:
            information_gathering()
        except (IndexError, PermissionError):
            continue


run()
