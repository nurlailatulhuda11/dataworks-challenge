import pandas as pd
from pathlib import Path

# Folder dataset dan output
DATA_DIR = Path("data")
OUTPUT_DIR = Path("outputs")
OUTPUT_DIR.mkdir(exist_ok=True)

# Baca dataset pengeluaran
df = pd.read_csv(DATA_DIR / "production_history.csv")

# Tukar Date kepada format tarikh
df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

# Nama lajur pengeluaran yang dijangka
production_cols = [
    "Oil_Rate",
    "Gas_Rate",
    "Water_Rate",
    "Water_Injection_Rate"
]

# Pastikan nilai pengeluaran berbentuk nombor
for col in production_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# Paparkan saiz dataset
print("Dataset shape:")
print(df.shape)

# Periksa nilai kosong
print("\nMissing values:")
print(df.isnull().sum())

# Paparkan statistik asas
print("\nSummary statistics:")
print(df[production_cols].describe())

# Susun data mengikut tarikh
df = df.sort_values("Date")

# Simpan dataset yang telah diproses
df.to_csv(
    OUTPUT_DIR / "production_history_clean.csv",
    index=False
)

print("\nCleaned production history saved.")
