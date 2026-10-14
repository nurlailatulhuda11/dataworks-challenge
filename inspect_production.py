import pandas as pd

xls = pd.ExcelFile("02 Field Production.xlsx")
for name in xls.sheet_names:
    df = xls.parse(name, nrows=5)
    print(f"\n=== {name} === lajur: {list(df.columns)[:8]}")
    print(df.head(3))