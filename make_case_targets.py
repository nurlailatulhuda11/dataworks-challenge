import pandas as pd

SRC = "data/reservoir_cases/02 Field Production.xlsx"
sheets = [
    "Gas production cumulative", "Oil production cumulative", "Water production cumulative",
    "Gas production rate", "Oil production rate", "Water production rate",
]

for s in sheets:
    df = pd.read_excel(SRC, sheet_name=s, header=1)
    df = df.iloc[1:].reset_index(drop=True)
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df = df.dropna(subset=["Date"])
    name = s.lower().replace(" ", "_")
    df.to_csv(f"data/{name}.csv", index=False)
    print(s, df.shape, df["Date"].min(), df["Date"].max())