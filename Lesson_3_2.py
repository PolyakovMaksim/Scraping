from pymongo import MongoClient
from pprint import pprint

client = MongoClient('127.0.0.1', 27017)
db = client['Vacancy']
hh_vacancy = db.hh_vacancy

int_sallary = int(input('Введите желаемый оклад: '))

for el in hh_vacancy.find({ '$or': [ { 'min_salary': { '$gt': int_sallary } }, { 'max_salary' : { '$gt': int_sallary } } ] }):
    pprint(el)