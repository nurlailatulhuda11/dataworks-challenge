import os
from datetime import datetime
import numpy as np
import pandas as pd
from openpyxl import load_workbook

N_FIT = 8
LO, HI = 0.90, 1.03            # had kaedah lama (setiap suku tahun)
LIQ_LO, LIQ_HI = 0.98, 1.01    # had jumlah cecair v2
WC_MAX = 0.99
SLOPE_MAX = 0.30               # kecerunan logit maksimum setiap suku tahun


def load(name):
    return pd.read_csv(f"data/quarterly_{name}.csv", parse_dates=["Date"], index_col="Date")


def integrate(cum_last, last_date, new_dates, rate_last, rates):
    all_rates = np.concatenate([[rate_last], rates])
    all_dates = pd.DatetimeIndex([last_date]).append(pd.DatetimeIndex(new_dates))
    days = np.diff(all_dates.values).astype("timedelta64[D]").astype(float)
    return cum_last + np.cumsum(0.5 * (all_rates[:-1] + all_rates[1:]) * days)


def growth(series):
    r = np.asarray(series, dtype=float)[-N_FIT:]
    if len(r) >= 3 and r.min() > 0:
        return float(np.exp(np.polyfit(np.arange(len(r)), np.log(r), 1)[0]))
    return 1.0


# ---------- Kaedah lama (setiap fasa berasingan) ----------
def forecast_old(rate_hist, cum_last, last_date, new_dates):
    r = np.asarray(rate_hist, dtype=float)
    g = float(np.clip(growth(r), LO, HI))
    k = np.arange(1, len(new_dates) + 1)
    return integrate(cum_last, last_date, new_dates, r[-1], r[-1] * g ** k)


# ---------- Kaedah v2 (jumlah cecair + water cut) ----------
def forecast_v2(oil_r, wat_r, gas_r, cum_last, last_date, new_dates):
    oil_r = np.asarray(oil_r, dtype=float)
    wat_r = np.asarray(wat_r, dtype=float)
    gas_r = np.asarray(gas_r, dtype=float)
    liq = oil_r + wat_r
    k = np.arange(1, len(new_dates) + 1)

    g_liq = float(np.clip(growth(liq), LIQ_LO, LIQ_HI))
    liq_f = liq[-1] * g_liq ** k

    wc = np.clip(wat_r / np.where(liq > 0, liq, np.nan), 1e-4, 0.999)
    wc = np.nan_to_num(wc, nan=1e-4)
    logit = np.log(wc / (1 - wc))[-N_FIT:]
    slope = np.polyfit(np.arange(len(logit)), logit, 1)[0] if len(logit) >= 3 else 0.0
    slope = float(np.clip(slope, 0.0, SLOPE_MAX))
    wc_f = np.minimum(1 / (1 + np.exp(-(logit[-1] + slope * k))), WC_MAX)

    oil_f = liq_f * (1 - wc_f)
    wat_f = liq_f * wc_f
    gor = gas_r[-1] / oil_r[-1] if oil_r[-1] > 0 else 0.0
    gas_f = oil_f * gor

    return {
        "Oil": integrate(cum_last["Oil"], last_date, new_dates, oil_r[-1], oil_f),
        "Water": integrate(cum_last["Water"], last_date, new_dates, wat_r[-1], wat_f),
        "Gas": integrate(cum_last["Gas"], last_date, new_dates, gas_r[-1], gas_f),
    }


PH = {"Gas": "gas_production", "Oil": "oil_production", "Water": "water_production"}
rate = {p: load(f"{f}_rate") for p, f in PH.items()}
cumu = {p: load(f"{f}_cumulative") for p, f in PH.items()}
dates = rate["Oil"].index
last_date = dates[-1]


def run_v2(col, upto, new_dates):
    cl = {p: cumu[p][col].iloc[upto] for p in PH}
    return forecast_v2(rate["Oil"][col].values[: upto + 1], rate["Water"][col].values[: upto + 1],
                       rate["Gas"][col].values[: upto + 1], cl, dates[upto], new_dates)


# ---------- Backtest: potong 8 suku tahun sebelum akhir ----------
cut = len(dates) - 1 - 8
print("Backtest (potong pada", dates[cut].date(), ", ramal 8 suku tahun)")
print("Ralat peratus median bagi kumulatif akhir:")
for p in PH:
    e_old, e_new = [], []
    for c in rate[p].columns:
        true = cumu[p][c].iloc[-1]
        if true <= 0:
            continue
        old = forecast_old(rate[p][c].values[: cut + 1], cumu[p][c].iloc[cut],
                           dates[cut], dates[cut + 1:])[-1]
        new = run_v2(c, cut, dates[cut + 1:])[p][-1]
        e_old.append(abs(old - true) / true)
        e_new.append(abs(new - true) / true)
    print(f"  {p:6s} lama = {np.median(e_old):.2%}   v2 = {np.median(e_new):.2%}")

# ---------- Isi template ----------
wb = load_workbook("09 Template Deliverable.xlsx")
for ws in wb.worksheets:
    case = int(ws.title.split()[-1])
    col = f"Case_{case}"
    cols = {}
    for c in range(1, ws.max_column + 1):
        h = str(ws.cell(1, c).value or "")
        for p in PH:
            if h.startswith(p):
                cols[p] = c
    new_dates = []
    for r in range(2, ws.max_row + 1):
        v = ws.cell(r, 1).value
        if v is None:
            break
        new_dates.append(v if isinstance(v, datetime) else datetime.strptime(str(v), "%m/%d/%Y"))
    res = run_v2(col, len(dates) - 1, new_dates)
    for p, c in cols.items():
        for i, val in enumerate(res[p]):
            ws.cell(2 + i, c).value = float(val)

os.makedirs("outputs", exist_ok=True)
wb.save("outputs/Deliverable_filled_v2.xlsx")
print("Siap: outputs/Deliverable_filled_v2.xlsx,", len(wb.worksheets), "worksheet")

# Ringkasan water cut 2028 untuk semakan
chk = pd.read_excel("outputs/Deliverable_filled_v2.xlsx", sheet_name="Case 1")
print("\nCase 1 (v2), 3 baris terakhir:")
print(chk.tail(3).to_string(index=False))