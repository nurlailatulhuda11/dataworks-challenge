
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

DATA_DIR = Path("data")
OUTPUT_DIR = Path("outputs")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(DATA_DIR / "production_history.csv")

# Pastikan lajur tarikh wujud
if "Date" not in df.columns:
    raise ValueError("Dataset mesti mempunyai lajur Date.")

df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

# Nama lajur yang dijangka dalam CSV
pproduction_cols = [
    "Oil production rate (STB/d)",
    "Gas production rate (MSCF/d)",
    "Water production rate (STB/d)",
    "Water injection rate (STB/d)",
]

# Semak sama ada semua lajur tersedia
missing_cols = [
    col for col in production_cols if col not in df.columns
]

if missing_cols:
    raise ValueError(
        f"Lajur berikut tiada dalam CSV: {missing_cols}. "
        "Sesuaikan nama lajur dalam kod dengan dataset asal."
    )

# Tukar kepada nombor
for col in production_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")

df = df.sort_values("Date")

print("Jumlah rekod:", len(df))
print("\nStatistik pengeluaran:")
print(df[production_cols].describe())

print("\nNilai kosong:")
print(df[production_cols].isnull().sum())

# Simpan data tersusun
df.to_csv(
    OUTPUT_DIR / "production_history_clean.csv",
    index=False
)

# Graf setiap jenis kadar pengeluaran
for col in production_cols:
    plt.figure(figsize=(10, 5))
    plt.plot(df["Date"], df[col])
    plt.title(col.replace("_", " ") + " Over Time")
    plt.xlabel("Date")
    plt.ylabel("Rate")
    plt.grid(True)
    plt.tight_layout()

    safe = col.split(" (")[0].lower().replace(" ", "_")
    filename = OUTPUT_DIR / f"{safe}_plot.png"
    plt.savefig(filename)
    plt.close()

print("\nData bersih dan graf telah disimpan dalam outputs.")
