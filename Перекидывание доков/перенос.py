import pathlib
import shutil
import os


def di1():
    """Функция указания начальной точки пути и проверяющая путь к исходной директории и наличие файлов в ней

    direct_all - список директорий корневой директории (lst)
    a - название исходной директории (str)
    lst_file - список файлов в исходной директории (lst)
    :return название существующей директории (str)
    """
    direct_all = os.listdir()   # вызываем список содержимого в корневой папке
    while True:
        a = input('Введите название директории с файлами: ')
        for i in direct_all:
            if i == a:
                lst_file = []
                for file in pathlib.Path(a).glob('*.*'):    # вынимаем из указанного пути папки все файлы
                    lst_file.append(file)
                if len(lst_file) == 0:
                    print('В директории нету файлов')
                    break
                else:
                    return a
        else:
            print('Такой директории не существует попробуйте заново или в ней нету файлов...')


def di2():
    """Функция указания конечной точки пути и проверяющая существование его. Если не существует то создает
    директорию.

    direct_all - список директорий корневой директории (lst)
    dir2 - название конечной директории (str)
    :return название конечной директории
    """
    direct_all = os.listdir()
    count = 0
    dir2 = input('Введите директорию куда файл будет перенесен: ')
    for i in direct_all:
        if i != dir2:
            count += 1
        else:
            return dir2
    if count == len(direct_all):
        os.mkdir(dir2)
        return dir2


def bye_bye(path1: str, suf: str, path2: str):
    """Функция осуществляющая перемещение файлов указываемого типа из начальной директории в конечную

    path1 - начальная директория (str)
    path2 - конечная директория (str)
    suf - тип документа (str)
    :return none
    """
    for file in pathlib.Path(path1).glob(f'*.{suf}'):   # достаем из директории только нужный нам тип
        shutil.move(file, path2)    # перемещаем то что достали в указанную директорию


bye_bye(di1(), input('Введите тип файла: ').rstrip().replace('.', ''), di2())
