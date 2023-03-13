import csv
import random
import pyttsx3

def quest_stat(dict1, dict_section, count):
    '''
    Создание/добавление 'key' категории вопроса в словарь-счетчик и добавление в
     'value' количество вопросов

    :param dict1 - словарь - счётчик
    :param dict_section - категория ключ
    :param count - значение изменения счетсика
    :return  словарь-счетчик[категория вопроса]: количество вопросов
    '''
    # если в словаре нет такого ключа
    if dict1.get(dict_section, False) is False:
        dict1[dict_section] = count
        # если такой ключ уже есть
    else:
        value = dict1[dict_section] + count
        dict1[dict_section] = value


def percent_answered(quest_total, quest_answered):
    '''
    Подсчёт процента ответов по категории

    :param quest_total: словарь-счетчик - Всего вопросов по категории
    :param quest_answered: словарь-счетчик - Всего положительных ответов по
            категории
    :return: Процент ответов по каждой категории вопросов
    '''
    for key in quest_total.keys():
        if key in quest_answered.keys():
            quest_percent_answered[key] = (quest_answered[key] * 100
                                          / quest_total[key])
            print(f'{key} - {quest_percent_answered[key]} % ответов')


# инициализация движка
engine = pyttsx3.init()
# инициализация свойств
engine.setProperty('rate', 200)     # скорость речи, слов в минуту
engine.setProperty('volume', 1.0)   # громкость (0-1)

try:
    with open("it_question.csv", encoding='utf-8') as r_file:
        # Создаем объект словарь DictReader, указываем символ-разделитель ","
        file_reader = csv.DictReader(r_file, delimiter=";")
        quest_list = list(file_reader)
except IOError as err:
    print("Error:", err)
    print("Code:", err.errno)


quest_total = {} # словарь-счетчик - Всего вопросов по категории
quest_answered = {} # словарь-счетчик - Всего положительных ответов по категории
quest_percent_answered = {} # словарь-счетчик % ответов по категории

while True:
    if quest_list != []:
        quest = random.choice(quest_list)
        quest_1 = f'Вопрос {quest["id"]} - раздел "{quest["section"]}"\n{quest["question"]} '
        print(quest_1)
        print("1 - Ответили на вопрос, 2 - пропустить вопрос, 9 - закончить : ")
        engine.say(quest_1)
        engine.runAndWait()
        _ = input()
        # удаление заданного вопроса
        quest_list = [{**row} for row in quest_list if row["id"] != quest["id"]]
        # добавление к счетчику - всего вопросов
        quest_stat(quest_total, quest["section"], 1)
        if _ == '1':
            # добавление к счетчику - положительных ответов
            quest_stat(quest_answered, quest["section"], 1)
        elif _ == '9':
            print("Досрочное завершение. ")
            break
        else:
            # инициируется счетчик или остается предыдущее значение
            quest_stat(quest_answered, quest["section"], 0)
    else:
        exit_text = 'Вопросов больше нет.'
        print(exit_text)
        engine.say(exit_text, '\n\n ')
        engine.runAndWait()
        break

# вывод статистики ответов
print(f'\n\nВсего было вопросов - {sum(quest_total.values())}')
percent = sum(quest_answered.values()) * 100 // sum(quest_total.values())
print(f'Вы дали ответ на {sum(quest_answered.values())} ({percent}%) вопросов')
print(f'\nПодробнее по категориям вопросов:')
percent_answered(quest_total, quest_answered)
