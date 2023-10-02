import csv
import pandas as pd
import requests
from bs4 import BeautifulSoup
import re

dt = {} # уникальные слова из каждой статьи
un_words = dict() # слова, которые записываются в csv-файл
count = 0
k = 0


def isPreposition_or_Conjuction(text):  # функция, которая проверяет, не является ли слово предлогом/союзом
    if text in ['в', 'без', 'до', 'для', 'за', 'через', 'над', 'по',
                'из', 'у', 'около', 'под', 'о', 'про', 'на', 'к', 'перед', 'при', 'с', 'между',
                'и', 'лишь', 'пока', 'когда', 'что', 'потому', 'почему', 'притом', 'причем',
                'поэтому', 'чтоб', 'чтобы', 'а', 'но', 'или' 'когда', 'если' 'то']:

        return True
    else:
        return False


def clearPunctuationMark(text):  # функция, которая очищает входной параметр от зноков пунктуации
    # marks = [',', '.', ':', ';', '?', '«', '»', '(', ')', '!', '\"', '“', '”', '—', '-', '+', '/', '–', '​', '„',
             # '“', '…', '№', '­']

    n_word = re.sub('[,|.|:|;|?|«|»|(|)|!|"|“|”|—|-|+|/|–|​|„|“|…|№|­]', "", text)
    return n_word

def match(text, alphabet=set('абвгдеёжзийклмнопрстуфхцчшщъыьэюя')):
    return not alphabet.isdisjoint(text.lower())


if __name__ == '__main__':
    with open('stat.csv', encoding='utf-8', newline='') as csvfile:  # открываем файл, в котором ссылки на статьи,
        # включающие слова-токены
        reader = csv.reader(csvfile) # читаем csv-файл
        for row in reader:
            if count == 10:
                break
            # try:
            if row == ['', 'Links', 'Words']:  # первую строчку пропускаем, чтобы не мешала парсить
                continue
            else:
                print(row[0])
                response = requests.get(url=row[1])  # делаем запрос по извлечённой ссылке
                response.encoding = 'utf-8'
                soup = BeautifulSoup(response.text, 'lxml')
                article_text = soup.find('div', class_='article')  # получаем текст статьи
                article_text.find_all()
                for word in str(article_text.text).split():  # разделяем текст по пробелам
                    article_elem = word.lower()  # каждое слово в нижний регистр
                    keys = dt.keys()  # распределяем слова по словарю dt
                    if article_elem in keys:
                        dt[article_elem] += 1
                    else:
                        dt[article_elem] = 1

                # print(dt)

                sorted_dict = dict(sorted(dt.items(), key=lambda elem: elem[1]))  # нужно оставить только уникальные
                # слова, предварительно сортируем словарь
                for key in sorted_dict.keys():  # теперь key - это наше уникальное слово
                    if sorted_dict.get(key) > 1:
                        break
                    else:
                        new_word = clearPunctuationMark(key)  # очищаем key от знаков препинания и записываем в new_word
                        if not isPreposition_or_Conjuction(new_word) and len(new_word) > 3:  # проверяем, является
                            # ли слово предлогом/союзом, а также смотрим на его длину
                            k = 0
                            for char in new_word:
                                if match(text=char):  # только слова, состоящие из кириллицы, записываем в словарь
                                    # un_words
                                    k += 1
                            if k == len(new_word):
                                if new_word in un_words.keys():  # и также добавляем в словарь un_words все слова
                                    un_words[new_word] += 1
                                else:
                                    un_words[new_word] = 1

                # print(un_words)
                # count += 1
                dt.clear()  # очищаем наш словарь dt при переходе на новую строку в csv файле
                # print(dt)

    frame = {'Words': pd.Series(un_words.keys()), 'Frequency': pd.Series(un_words.values())}
    df = pd.DataFrame(frame)
    filename = 'words.csv'
    df.to_csv(filename)
