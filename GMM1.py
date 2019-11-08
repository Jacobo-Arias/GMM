import pandas as pd 
import json

xls = pd.read_csv('datos.csv',na_values=['no info','.']#,index_col='Month'
                    )

# xls.head(#)
# meses= xls['Month']
print(xls)


with open('datos.json') as json_file:
    data = json.load(json_file)
#     for i in data:
#         print (i)