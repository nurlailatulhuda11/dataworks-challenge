
from pathlib import Path
import pandas as pd

# Folder projek
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" / "reservoir_cases"
OUTPUT_DIR = BASE_DIR / "outputs"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def analyze_reservoir():
    print("=" * 60)
    print("RESERVOIR DATA ANALYSIS")
    print("=" * 60)

    # Cari semua fail Excel
    excel_files = [
        file for file in DATA_DIR.iterdir()
        if file.suffix.lower() in [".xlsx", ".xls"]
        and not file.name.startswith("~$")
    ] if DATA_DIR.exists() else []

    if not excel_files:
        print(f"ERROR: Tiada fail Excel dijumpai dalam {DATA_DIR}")
        print("Sila semak lokasi folder dan fail Excel.")
        return

    all_data = []
    file_summaries = []

    for file in sorted(excel_files):
        print(f"\nReading file: {file.name}")

        try:
            # Baca semua worksheet dalam fail Excel
            sheets = pd.read_excel(file, sheet_name=None)

            for sheet_name, df in sheets.items():
                if df.empty:
                    print(f"  Sheet '{sheet_name}' kosong. Skip.")
                    continue

                # Buang ruang kosong pada nama lajur
                df.columns = [
                    str(col).strip() for col in df.columns
                ]

                # Buang baris dan lajur yang kosong sepenuhnya
                df = df.dropna(how="all")
                df = df.dropna(axis=1, how="all")

                # Tambah maklumat sumber data
                df["Case_File"] = file.name
                df["Sheet_Name"] = sheet_name

                # Simpan data bagi setiap worksheet
                safe_name = (
                    f"{file.stem}_{sheet_name}"
                    .replace(" ", "_")
                    .replace("/", "_")
                    .replace("\\", "_")
                )

                output_csv = OUTPUT_DIR / f"{safe_name}.csv"
                df.to_csv(output_csv, index=False)

                # Pilih lajur numerik untuk analisis
                numeric_df = df.select_dtypes(
                    include="number"
                )

                # Kira maklumat kualiti data
                missing_values = int(df.isna().sum().sum())
                duplicate_rows = int(
                    df.drop(columns=["Case_File", "Sheet_Name"])
                    .duplicated()
                    .sum()
                )

                print(f"  Worksheet: {sheet_name}")
                print(f"  Rows: {len(df)}")
                print(f"  Columns: {len(df.columns)}")
                print(f"  Missing values: {missing_values}")
                print(f"  Duplicate rows: {duplicate_rows}")

                file_summaries.append({
                    "Case_File": file.name,
                    "Sheet_Name": sheet_name,
                    "Rows": len(df),
                    "Columns": len(df.columns),
                    "Missing_Values": missing_values,
                    "Duplicate_Rows": duplicate_rows
                })

                # Simpan statistik parameter numerik
                if not numeric_df.empty:
                    stats = numeric_df.describe().T
                    stats.index.name = "Parameter"
                    stats.reset_index(inplace=True)
                    stats["Case_File"] = file.name
                    stats["Sheet_Name"] = sheet_name

                    stats.to_csv(
                        OUTPUT_DIR / f"{safe_name}_statistics.csv",
                        index=False
                    )

                all_data.append(df)

        except Exception as error:
            print(f"  ERROR reading {file.name}: {error}")

    # Simpan laporan kualiti data
    if file_summaries:
        summary_df = pd.DataFrame(file_summaries)
        summary_df.to_csv(
            OUTPUT_DIR / "reservoir_quality_report.csv",
            index=False
        )

    # Gabungkan semua worksheet untuk analisis keseluruhan
    if all_data:
        combined_df = pd.concat(
            all_data,
            ignore_index=True,
            sort=False
        )

        combined_df.to_csv(
            OUTPUT_DIR / "reservoir_all_cases.csv",
            index=False
        )

        print("\nCombined dataset saved.")
        print(f"Total rows: {len(combined_df)}")
        print(f"Total columns: {len(combined_df.columns)}")

        # Ringkasan parameter reservoir yang biasa digunakan
        reservoir_parameters = [
            "PORO", "PORV", "PERMX", "PERMY",
            "PERMZ", "NTG", "TRANX"
        ]

        available_parameters = [
            col for col in reservoir_parameters
            if col in combined_df.columns
        ]

        if available_parameters:
            parameter_summary = (
                combined_df[available_parameters]
                .apply(pd.to_numeric, errors="coerce")
                .describe()
                .T
            )

            parameter_summary.index.name = "Parameter"
            parameter_summary.reset_index(inplace=True)

            parameter_summary.to_csv(
                OUTPUT_DIR / "reservoir_parameter_summary.csv",
                index=False
            )

            print("\nReservoir parameter summary:")
            print(parameter_summary.to_string(index=False))
        else:
            print(
                "\nStandard reservoir parameters were not found "
                "using their expected column names."
            )

    print("\nAnalysis completed.")
    print(f"Check output files in: {OUTPUT_DIR}")


if __name__ == "__main__":
    analyze_reservoir()
