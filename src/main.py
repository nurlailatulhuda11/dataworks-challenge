
from data_preparation import (
    prepare_production_history,
    prepare_reservoir_cases
)

import subprocess
import sys


def main():
    print("STARTING DATAWORKS CHALLENGE PIPELINE")

    print("\nSTEP 1: Preparing datasets")
    prepare_production_history()
    prepare_reservoir_cases()

    print("\nSTEP 2: Production history analysis")
    subprocess.run(
        [sys.executable, "src/production_history.py"],
        check=True
    )

    print("\nSTEP 3: Reservoir parameter analysis")
    subprocess.run(
        [sys.executable, "src/reservoir_analysis.py"],
        check=True
    )

    print("\nPIPELINE COMPLETED")


if __name__ == "__main__":
    main()
