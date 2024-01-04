import pandas as pd
df = pd.read_csv("./Main.csv")
columns  = df.columns
columns_list = []
for i in range(1,len(columns)):
    columns_list.append((f'{i}',columns[i]))