import requests
import re
from bs4 import BeautifulSoup as bs
from pymongo import MongoClient
import datetime
import hashlib

now = datetime.datetime.now()

client = MongoClient('127.0.0.1', 27017)
db = client['Vacancy']
hh_vacancy = db.hh_vacancy

position_name = input('Введите название должности: ')
position_name = '+'.join(position_name.split(' '))
number_page = input('Введите количество страниц для вывода : ')
my_headers = {
    'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'}
reg = requests.get('https://hh.ru/search/vacancy?items_on_page=20&area=1&text=' + position_name, headers=my_headers)

i = 0
for i in range(int(number_page)):
    if reg.ok:
        source = 'https://hh.ru'
        soup = bs(reg.text, 'html.parser')
        serials = soup.find_all('div', {'class': 'vacancy-serp-item'})
        for serial in serials:
            vacancu_name = serial.find('a', {'class': 'bloko-link'}).text
            try:
                employer = serial.find('a', {'class': 'bloko-link bloko-link_secondary'}).text
            except:
                employer = None
            location = serial.find('span', {'class': 'vacancy-serp-item__meta-info'}).text
            link = serial.find('a', {'class': 'bloko-link'}).get('href')
            try:
                salary = serial.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'}).text
                split_text = re.split(' |\u202f', salary)
                currency = split_text[-1]
                if split_text[0].isdigit():
                    count = 0
                    min_salary = ''
                    max_salary = ''
                    while split_text[count].isdigit():
                        min_salary = min_salary + split_text[count]
                        count += 1
                    count += 1
                    while split_text[count].isdigit():
                        max_salary = max_salary + split_text[count]
                        count += 1
                    min_salary = int(min_salary)
                    max_salary = int(max_salary)
                elif split_text[0] == 'до':
                    count = 1
                    min_salary = None
                    max_salary = ''
                    while split_text[count].isdigit():
                        max_salary = max_salary + split_text[count]
                        count += 1
                    max_salary = int(max_salary)
                else:
                    count = 1
                    min_salary = ''
                    max_salary = None
                    while split_text[count].isdigit():
                        min_salary = min_salary + split_text[count]
                        count += 1
                    min_salary = int(min_salary)
            except:
                salary = None
                max_salary = None
                min_salary = None
                currency = None

            my_dict = {'vacancu_name': vacancu_name, 'min_salary': min_salary, 'max_salary': max_salary,
                       'currency': currency, 'employer': employer,
                       'location': location}

            vacancy_hash = hashlib.sha1() # Для дедублицирования, link специально не взял, на случай замены
            vacancy_hash.update(repr(my_dict).encode('utf-8'))

            try:

                hh_vacancy.insert_one({'_id': vacancy_hash, 'vacancu_name': vacancu_name, 'link': link, 'source': source,
                       'min_salary': min_salary,
                       'max_salary': max_salary, 'currency': currency, 'employer': employer,
                       'location': location, 'create_date': str(now.date())})
            except:
                continue
        i += 1
        reg = requests.get(
            'https://hh.ru/search/vacancy?items_on_page=20&area=1&text=' + position_name + '?&page=' + str(i),
            headers=my_headers)
