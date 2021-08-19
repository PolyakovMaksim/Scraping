import requests
import json
user_name = input('Введите имя пользователя: ')
reg = requests.get(f'https://api.github.com/users/{user_name}/repos')
if reg.ok:
    data = json.loads(reg.text)
    my_list = []
    for i in range(len(data)):
        my_list.append(data[i]['name'])
    print (my_list)
    with open(f'{user_name}.json', 'w') as write_f:
        json.dump(my_list, write_f)