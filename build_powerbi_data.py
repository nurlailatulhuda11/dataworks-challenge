import os
import pandas as pd

CASES = range(1, 11)
PHASES = ["gas", "oil", "water"]
os.makedirs("powerbi", exist_ok=True)

# Sejarah (1998-2008) dan ramalan (2008-2028), format panjang
rows = []
for ph in PHASES:
    q = pd.read_csv(f"data/quarterly_{ph}_production_cumulative.csv",
                    parse_dates=["Date"], index_col="Date")
    for c in CASES:
        s = q[f"Case_{c}"]
        rows.append(pd.DataFrame({"Case": c, "Date": s.index, "Phase": ph.capitalize(),
                                  "Cumulative": s.values, "Type": "History"}))

fc = pd.read_excel("outputs/Deliverable_filled.xlsx", sheet_name=None)
for name, df in fc.items():
    case = int(name.split()[-1])
    d = df["Date"]
    dates = d if pd.api.types.is_datetime64_any_dtype(d) else pd.to_datetime(d, format="%m/%d/%Y")
    for col in df.columns[1:4]:
        rows.append(pd.DataFrame({"Case": case, "Date": dates,
                                  "Phase": col.split()[0],
                                  "Cumulative": df[col].values, "Type": "Forecast"}))

out = pd.concat(rows, ignore_index=True)
out["Year"] = out["Date"].dt.year
out.sort_values(["Case", "Phase", "Date"]).to_csv("powerbi/production_long.csv", index=False)

# Kadar sejarah
rr = []
for ph in PHASES:
    q = pd.read_csv(f"data/quarterly_{ph}_production_rate.csv", parse_dates=["Date"], index_col="Date")
    for c in CASES:
        rr.append(pd.DataFrame({"Case": c, "Date": q.index, "Phase": ph.capitalize(),
                                "Rate": q[f"Case_{c}"].values}))
pd.concat(rr).to_csv("powerbi/rate_history.csv", index=False)

# Ciri reservoir bagi 10 kes
f = pd.read_csv("data/case_features.csv")
f[f["case"].isin(CASES)][["case", "porv_sum", "oil_in_place",
                          "Porosity (PORO)_mean", "Permeability I (PERMX)_mean"]
  ].to_csv("powerbi/case_features.csv", index=False)

print(out.groupby(["Type", "Phase"]).size())
print("Siap: folder powerbi/")