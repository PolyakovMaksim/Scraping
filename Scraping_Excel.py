# Вылетает предупреждение о использовании различных стилей в документе, если не открыть файл и не разрешить редактирование, но программа отрабатывает
# Не придумал еще как закинуть много файлов (если они все одностраничные, то решение есть)
import pandas as pd


file_name = ('konta izraksts Azon Business.xlsx')
name_sheets = ['Sheet1']

for name_sheet in name_sheets:
    df = pd.read_excel(io = file_name, sheet_name = name_sheet)
    df = df.rename(columns = {'Unnamed: 1' : 'col2'})

    flag = df.col2.str.find('Izejosais pärskaitijums ( # 183 )')
    index = df[flag > 0 ].index.tolist()
    print(df.loc[index])