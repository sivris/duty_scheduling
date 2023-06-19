import pandas as pd

df = pd.read_excel(r'sort_data.xlsx')

for name in df.loc[:, 'weekdays A']:
    print(name)
