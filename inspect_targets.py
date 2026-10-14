import pandas as pd

df = pd.read_csv("data/oil_production_cumulative.csv", parse_dates=["Date"])
print("Lajur (5 pertama, 5 terakhir):", list(df.columns[:5]), list(df.columns[-5:]))
print("Tarikh unik:", df["Date"].nunique(), "daripada", len(df), "baris")
print(df["Date"].value_counts().head())
print(df[["Date", df.columns[1], df.columns[2]]].iloc[[0, 1, 2, 3, 100, 1000, 5000, -1]])
print("Nilai kosong per lajur (teratas):")
print(df.isna().sum().sort_values(ascending=False).head())