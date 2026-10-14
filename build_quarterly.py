import pandas as pd

targets = ["gas_production_cumulative", "oil_production_cumulative",
           "water_production_cumulative", "gas_production_rate",
           "oil_production_rate", "water_production_rate"]

hist = pd.read_csv("data/production_history.csv", parse_dates=["Date"])
qdates = pd.DatetimeIndex(hist["Date"])

for t in targets:
    df = pd.read_csv(f"data/{t}.csv", parse_dates=["Date"]).set_index("Date")
    df = df.drop(columns=["RAMP_History"], errors="ignore")
    out = {}
    for case in df.columns:
        s = df[case].dropna()
        s = s[~s.index.duplicated()]
        both = s.index.union(qdates)
        out[case] = s.reindex(both).interpolate("time").reindex(qdates)
    res = pd.DataFrame(out)
    res.index.name = "Date"
    res.to_csv(f"data/quarterly_{t}.csv")
    print(t, res.shape, "NaN:", int(res.isna().sum().sum()))