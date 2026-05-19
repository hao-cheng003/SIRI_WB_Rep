from pathlib import Path
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]

LBP_FILE = PROJECT_ROOT / "data" / "processed" / "balu_nocrop" / "balu_lbp59_nocrop.csv"
BSIF_FILE = PROJECT_ROOT / "data" / "processed" / "bsif_bits_sweep_nocrop" / "balu_bsif_9x9_10bit_nocrop.csv"

OUT_DIR = PROJECT_ROOT / "data" / "processed" / "final_features"
OUT_FILE = OUT_DIR / "balu_lbp59_bsif_9x9_10bit_nocrop.csv"

META_COLS = [
    "filename",
    "relative_path",
    "sample_id",
    "severity",
    "binary_label",
    "binary_name",
]


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    lbp_df = pd.read_csv(LBP_FILE)
    bsif_df = pd.read_csv(BSIF_FILE)

    # Make sure rows match
    if not lbp_df["filename"].equals(bsif_df["filename"]):
        raise ValueError("LBP and BSIF rows do not match. Check file ordering.")

    meta = lbp_df[META_COLS]

    lbp_features = lbp_df[[c for c in lbp_df.columns if c not in META_COLS]]
    bsif_features = bsif_df[[c for c in bsif_df.columns if c not in META_COLS]]

    # Rename to avoid duplicate names
    lbp_features = lbp_features.add_prefix("lbp_")
    bsif_features = bsif_features.add_prefix("bsif_")

    out_df = pd.concat([meta, lbp_features, bsif_features], axis=1)
    out_df.to_csv(OUT_FILE, index=False)

    print(f"Saved combined feature file to: {OUT_FILE}")
    print(f"Shape: {out_df.shape}")
    print(f"LBP features: {lbp_features.shape[1]}")
    print(f"BSIF features: {bsif_features.shape[1]}")
    print(f"Total features: {lbp_features.shape[1] + bsif_features.shape[1]}")


if __name__ == "__main__":
    main()