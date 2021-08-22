import requests
import re
from pandas import DataFrame as df
import json
from bs4 import BeautifulSoup as bs


position_name = input('Введите название должности на английском языке: ')
number_page = input('Введите количество страниц для вывода : ')
url = 'https://hh.ru'
my_headers = {'User-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'}

reg = requests.get(url+'/vacancies/'+ position_name, headers = my_headers)
vacancu_name_list = []
link_list = []
source_list = []
min_salar_list = []
max_salar_list = []
currency_list = []
employer_list = []
location_list = []
i = 0
for i in range(int(number_page)):
    if reg.ok:
        source = 'https://hh.ru'
        soup = bs(reg.text, 'html.parser')
        serials = soup.find_all('div', {'class': 'vacancy-serp-item'})
        serials_list = []
        for serial in serials:
            serial_data = {}
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
                    min_salar = ''
                    max_salar = ''
                    while split_text[count].isdigit():
                        min_salar = min_salar + split_text[count]
                        count += 1
                    count += 1
                    while split_text[count].isdigit():
                        max_salar = max_salar + split_text[count]
                        count += 1
                    min_salar = int(min_salar)
                    max_salar = int(max_salar)
                elif split_text[0] == 'до':
                    count = 1
                    min_salar = None
                    max_salar = ''
                    while split_text[count].isdigit():
                        max_salar = max_salar + split_text[count]
                        count += 1
                    max_salar = int(max_salar)
                else:
                    count = 1
                    min_salar = ''
                    max_salar = None
                    while split_text[count].isdigit():
                        min_salar = min_salar + split_text[count]
                        count += 1
                    min_salar = int(min_salar)
            except:
                salary = None
                max_salar = None
                min_salar = None
                currency = None

            vacancu_name_list.append(vacancu_name)
            link_list.append(link)
            source_list.append(source)
            min_salar_list.append(min_salar)
            max_salar_list.append(max_salar)
            currency_list.append(currency)
            employer_list.append(employer)
            location_list.append(location)
        i += 1
        reg = requests.get(url+'/vacancies/'+ position_name+'?page='+ str(i), headers=my_headers)

data = {'vacancu_name': vacancu_name_list, 'link' : link_list, 'source': source_list, 'min_salar': min_salar_list, 'max_salar': max_salar_list, 'currency' : currency_list, 'employer' : employer_list, 'location' : location_list}
frame = df(data)
with open(position_name+'.csv', 'w'):
   frame.to_csv(position_name+'.csv')
