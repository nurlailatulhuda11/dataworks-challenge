import os
import numpy as np
import pandas as pd
from sklearn.linear_model import Ridge

FEATS = ["oil_in_place", "porv_sum", "Permeability I (PERMX)_mean"]
TARGETS = ["oil_production_cumulative", "gas_production_cumulative",
           "water_production_cumulative"]
TRAIN = list(range(1, 71))
VAL = list(range(71, 86))
TEST = list(range(86, 101))


def predict_split(X, idx):
    """Latih Ridge dengan kes 1-70 sahaja, ramal kes dalam idx."""
    frames = []
    for t in TARGETS:
        Y = pd.read_csv(f"data/quarterly_{t}.csv", index_col="Date")
        Y.columns = [int(c.split("_")[1]) for c in Y.columns]
        pred = {}
        for d in Y.index:
            m = Ridge(alpha=1.0).fit(X.loc[TRAIN], Y.loc[d, TRAIN])
            pred[d] = m.predict(X.loc[idx])
        P = pd.DataFrame(pred, index=idx).T          # baris = tarikh, lajur = kes
        long = P.stack().rename("Predicted").reset_index()
        long.columns = ["Date", "Case", "Predicted"]
        long["Target"] = t
        long["Actual"] = [Y.loc[r.Date, r.Case] for r in long.itertuples()]
        frames.append(long)
    return pd.concat(frames, ignore_index=True)


def main():
    print("Memulakan proses ramalan Test Cases...")
    os.makedirs("outputs", exist_ok=True)

    X = pd.read_csv("data/case_features.csv").set_index("case")[FEATS]
    mu, sd = X.loc[TRAIN].mean(), X.loc[TRAIN].std()
    X = (X - mu) / sd

    for name, idx in (("validation", VAL), ("test", TEST)):
        out = predict_split(X, idx)
        path = f"outputs/{name}_predictions.csv"
        out.to_csv(path, index=False)

        last = out[out["Date"] == out["Date"].max()]
        mape = {}
        for t, g in last.groupby("Target"):
            g = g[g["Actual"] > 0]
            mape[t] = float((abs(g["Predicted"] - g["Actual"]) / g["Actual"]).mean())
        print(f"Disimpan: {path} {out.shape}")
        print("  MAPE pada tarikh akhir:",
              {k: f"{v:.2%}" for k, v in mape.items()})


if __name__ == "__main__":
    main()