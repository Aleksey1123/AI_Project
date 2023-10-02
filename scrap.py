import pandas as pd
from bs4 import BeautifulSoup
import requests

if __name__ == '__main__':

    links = []
    elements = []
    pool = ['спид', 'рак', 'инсульт', 'орви', 'диабет', 'covid-19', 'гепатит']
    # pool = ['гепатит']

    # url = 'https://minobrnauki.gov.ru/press-center/'
    root = 'https://medportal.ru'

    for i in range(1, 282):
        if i == 1:
            url = 'https://medportal.ru/mednovosti/all/'
        else:
            url = 'https://medportal.ru/mednovosti/all/?page=' + str(i)

        print(str(i) + ' / 281')
        response = requests.get(url=url)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'lxml')
        articles = soup.find_all('a', class_='title')

        for elem in articles:
            string = str(elem)
            index = string.find("\">", 23, len(string))
            href = string[23:index]
            link = root + href

            try:
                response = requests.get(url=str(link))
                soup = BeautifulSoup(response.text, 'lxml')
                article_text = soup.find('div', class_='article')
                for word in str(article_text.text).split():
                    article_elem = word.lower()
                    if article_elem in pool:
                        print('Статья подходит:')
                        print(link)
                        links.append(link)
                        elements.append(article_elem)
                        break
            except:
                continue

    frame = {'Links': pd.Series(links), 'Words': pd.Series(elements)}
    df = pd.DataFrame(frame)
    filename = 'stat.csv'
    df.to_csv(filename)
