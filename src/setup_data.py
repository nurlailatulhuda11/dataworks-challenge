from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
RESERVOIR_DIR = DATA_DIR / "reservoir_cases"
OUTPUT_DIR = BASE_DIR / "outputs"

PRODUCTION_FILE = RESERVOIR_DIR / "02 Field Production.xlsx"
EXPECTED_CASE_FILES = 6   # fail 03 hingga 08


def create_folders():
    for folder in (DATA_DIR, RESERVOIR_DIR, OUTPUT_DIR):
        folder.mkdir(parents=True, exist_ok=True)
    print("Project folders are ready.")


def make_production_history():
    df = pd.read_excel(PRODUCTION_FILE, sheet_name="Field Production")
    df = df.drop(columns=["Identifier"])
    df["Date"] = pd.to_datetime(df["Date"])
    out = DATA_DIR / "production_history.csv"
    df.to_csv(out, index=False)
    print(f"Saved {out} ({len(df)} rows)")


def check_reservoir_files():
    files = sorted(
        f for f in RESERVOIR_DIR.glob("*.xlsx")
        if f.name[:2] in {"03", "04", "05", "06", "07", "08"}
        and not f.name.startswith("~$")
    )
    print("\n--- Reservoir case files ---")
    for i, f in enumerate(files, 1):
        print(f"{i}. {f.name}")
    print(f"Total: {len(files)} (expected {EXPECTED_CASE_FILES})")


if __name__ == "__main__":
    create_folders()
    make_production_history()
    check_reservoir_files()
    print("\nSetup process finished.")