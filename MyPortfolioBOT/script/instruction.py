def read_inst() -> str:
    """Функция считывающая инструкцию для пользователя

    text - текст в инструкции (str)
    :return текст инструции (str)"""
    with open('Instruction.txt', encoding='UTF-8') as f:
        text = f.read()
        return text


