import pandas as pd

SRC = "data/reservoir_cases/02 Field Production.xlsx"

df = pd.read_excel(SRC, sheet_name="Field Production")
df = df.drop(columns=["Identifier"])
df["Date"] = pd.to_datetime(df["Date"])
df.to_csv("data/production_history.csv", index=False)
print(df.shape)
print(df.head())
print(df.tail())