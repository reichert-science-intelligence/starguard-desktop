"""
Create SDoH mapping dataset (ZIP -> barrier scores).
Uses AHRQ SDoH Database structure.
Run: python -m data.create_sdoh_mapping
Output: data/sdoh_mapping.csv
"""
import pandas as pd
import random
from pathlib import Path

# Base SDoH data - Pittsburgh + examples per AHRQ structure
SDOH_BASE = {
    "zip_code": ["15206", "15213", "15108", "90210", "10001"],
    "food_desert_score": [7.2, 3.1, 8.9, 1.2, 2.5],
    "transit_access_score": [4.5, 8.7, 2.1, 9.2, 9.8],
    "poverty_rate": [0.23, 0.11, 0.31, 0.05, 0.15],
    "uninsured_rate": [0.08, 0.04, 0.12, 0.03, 0.06],
    "primary_barrier": ["Transportation", "None", "Food Access", "None", "None"],
}


def expand_sdoh_data(base_df: pd.DataFrame, n_zips: int = 500) -> pd.DataFrame:
    """Expand base SDoH data to more ZIPs via interpolation."""
    expanded = []
    zips_seen = set(base_df["zip_code"].tolist())

    for _ in range(n_zips):
        base_row = base_df.sample(1).iloc[0]
        # Generate unique 5-digit ZIP
        while True:
            new_zip = f"{random.randint(10001, 99999)}"
            if new_zip not in zips_seen:
                zips_seen.add(new_zip)
                break
        expanded.append({
            "zip_code": new_zip,
            "food_desert_score": max(0, min(10, base_row["food_desert_score"] + random.uniform(-1, 1))),
            "transit_access_score": max(0, min(10, base_row["transit_access_score"] + random.uniform(-1, 1))),
            "poverty_rate": max(0, min(1, base_row["poverty_rate"] + random.uniform(-0.05, 0.05))),
            "uninsured_rate": max(0, min(1, base_row["uninsured_rate"] + random.uniform(-0.02, 0.02))),
            "primary_barrier": base_row["primary_barrier"],
        })

    return pd.DataFrame(expanded)


def main():
    script_dir = Path(__file__).parent
    base_df = pd.DataFrame(SDOH_BASE)
    sdoh_full = expand_sdoh_data(base_df)
    output_path = script_dir / "sdoh_mapping.csv"
    sdoh_full.to_csv(output_path, index=False)
    print(f"Created {len(sdoh_full)} SDoH mapping records at {output_path}")


if __name__ == "__main__":
    main()
