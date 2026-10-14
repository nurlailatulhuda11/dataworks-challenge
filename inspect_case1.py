import pandas as pd

path = "data/reservoir_cases/03 Train Cases 1.xlsx"
df = pd.read_excel(path, sheet_name="Case 1")

print("Semua lajur:")
for i, c in enumerate(df.columns, 1):
    print(i, c)

print("\nBilangan baris:", len(df))
active = df[df["Pore Volume (PORV)"] > 0]
print("Sel aktif (PORV > 0):", len(active))
print("\nRingkasan sel aktif:")
print(active.describe().T[["min", "mean", "max"]].to_string())