# Вылетает предупреждение о использовании различных стилей в документе, если не открыть файл и не разрешить редактирование, но программа отрабатывает
# Не придумал еще как закинуть много файлов (если они все одностраничные, то решение есть)
import pandas as pd


file_name = ('konta izraksts Azon Business.xlsx')
name_sheets = ['Sheet1']

for name_sheet in name_sheets:
    df = pd.read_excel(io = file_name, sheet_name = name_sheet)

    for el in df['Unnamed: 1']:  # 'Unnamed: 1' название колонки конкретно в этом файле, нужно поискать как используется индекс
        try:
            campaign = el.split('Izejosais pärskaitijums ( # 183 )')[1]
            print(campaign)
        except:
            continue
