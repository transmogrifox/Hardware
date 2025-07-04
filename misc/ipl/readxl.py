import pandas as pd

df = pd.read_excel('ipl_config.xlsx')

nrows = df.shape[0]

for r in range(nrows):
    typ = df.loc[r, 'Typ']
    name = df.loc[r, 'Parameter']
    mul = df.loc[r, 'Multiplier']
    unit = df.loc[r, 'Unit']

    if mul == 1:
        print(f"{name}\t{typ:.2f}\t{unit}")
    else:
        print(f"{name}\t{typ:.2f}\t{mul}{unit}")

#print(df)








