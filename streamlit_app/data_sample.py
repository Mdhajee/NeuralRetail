import pandas as pd
import numpy as np
from pathlib import Path

ROOT      = Path(r"C:\Users\sh85r\My Drive\OneDrive\Documents\NeuralRetail")
DATA_SAMPLE = Path(__file__).parent.parent / "data_sample"
SAMPLE    = ROOT / 'streamlit_app' / 'data_sample'
SAMPLE.mkdir(exist_ok=True)

# Keep only 1000 rows — tiny files for GitHub
files = [
    ('events_clean.parquet',         1000),
    ('segments.parquet',              1000),
    ('churn_scores.parquet',          1000),
    ('inventory_optimised.parquet',   1000),
    ('item_popularity.parquet',        1000),
    ('forecast_output.parquet',        None),
]

for fname, n in files:
    df = pd.read_parquet(DATA_SAMPLE / fname)
    df = df.head(n) if n else df
    df.to_parquet(SAMPLE / fname, index=False)
    size_kb = (SAMPLE / fname).stat().st_size / 1024
    print(f"✓ {fname}: {len(df)} rows  {size_kb:.0f} KB")

print("\nAll sample files created — safe for GitHub")