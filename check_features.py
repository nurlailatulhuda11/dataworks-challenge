import pandas as pd

f = pd.read_csv("data/case_features.csv").set_index("case")

print("Ciri yang BERUBAH antara kes (bilangan nilai unik > 1):")
nun = f.nunique()
print(nun[nun > 1].to_string())
print("\nCiri TETAP (buang):", list(nun[nun == 1].index))

y = pd.read_csv("data/quarterly_oil_production_cumulative.csv",
                parse_dates=["Date"]).set_index("Date")
final = y.iloc[-1]                       # kumulatif minyak pada 2008-01-01
final.index = [int(c.split("_")[1]) for c in final.index]

varying = f.loc[:, nun > 1]
corr = varying.corrwith(final.reindex(varying.index)).sort_values(key=abs, ascending=False)
print("\nKorelasi dengan minyak kumulatif akhir (2008-01-01):")
print(corr.to_string())