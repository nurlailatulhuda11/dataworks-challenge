import numpy as np
import pandas as pd
from sklearn.linear_model import Ridge
from sklearn.metrics import r2_score, mean_absolute_percentage_error

FEATS = ["oil_in_place", "porv_sum", "Permeability I (PERMX)_mean"]
TARGETS = ["oil_production_cumulative", "gas_production_cumulative",
           "water_production_cumulative"]

X = pd.read_csv("data/case_features.csv").set_index("case")[FEATS]
mu, sd = X.loc[1:70].mean(), X.loc[1:70].std()
X = (X - mu) / sd

tr, va, te = range(1, 71), range(71, 86), range(86, 101)

for t in TARGETS:
    Y = pd.read_csv(f"data/quarterly_{t}.csv", index_col="Date")
    Y.columns = [int(c.split("_")[1]) for c in Y.columns]
    scores = {}
    for name, idx in (("val", va), ("test", te)):
        preds = []
        for d in Y.index:                      # satu model bagi setiap tarikh
            m = Ridge(alpha=1.0).fit(X.loc[tr], Y.loc[d, tr])
            preds.append(m.predict(X.loc[idx]))
        P = pd.DataFrame(preds, index=Y.index, columns=list(idx))
        T = Y[list(idx)]
        mask = T.iloc[-1] > 0
        scores[name] = (r2_score(T.values.ravel(), P.values.ravel()),
                        mean_absolute_percentage_error(
                            T.iloc[-1][mask], P.iloc[-1][mask]))
    print(t, {k: f"R2={v[0]:.3f}, MAPE akhir={v[1]:.1%}" for k, v in scores.items()})