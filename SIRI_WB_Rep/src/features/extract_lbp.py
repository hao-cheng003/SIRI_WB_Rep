from pathlib import Path

import numpy as np
import pandas as pd
import tifffile as tiff
from skimage.feature import local_binary_pattern
from tqdm import tqdm


PROJECT_ROOT = Path(__file__).resolve().parents[1]
LABEL_CSV = PROJECT_ROOT / "data" / "labels.csv"
OUT_DIR = PROJECT_ROOT / "data" / "processed"
OUT_FILE = OUT_DIR / "lbp_features.csv"

P = 8
R = 1
N_BINS = P + 2


def extract_lbp_hist(img: np.ndarray) -> np.ndarray:

    if img.ndim != 2:
        raise ValueError(f"Expected grayscale image, got shape: {img.shape}")

    mask = img > 0

    lbp = local_binary_pattern(img, P=P, R=R, method="uniform")

    values = lbp[mask]

    hist, _ = np.histogram(
        values,
        bins=np.arange(0, N_BINS + 1),
        range=(0, N_BINS),
        density=False,
    )

    hist = hist.astype(np.float32)

    if hist.sum() > 0:
        hist = hist / hist.sum()

    return hist


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    labels = pd.read_csv(LABEL_CSV)

    records = []

    for _, row in tqdm(labels.iterrows(), total=len(labels)):
        img_path = PROJECT_ROOT / row["relative_path"]
        img = tiff.imread(img_path)

        features = extract_lbp_hist(img)

        record = {
            "filename": row["filename"],
            "relative_path": row["relative_path"],
            "sample_id": row["sample_id"],
            "severity": row["severity"],
            "binary_label": row["binary_label"],
            "binary_name": row["binary_name"],
        }

        for i, value in enumerate(features):
            record[f"lbp_{i:02d}"] = value

        records.append(record)

    df = pd.DataFrame(records)
    df.to_csv(OUT_FILE, index=False)

    print(f"Saved LBP features to: {OUT_FILE}")
    print(f"Feature table shape: {df.shape}")

    feature_cols = [c for c in df.columns if c.startswith("lbp_")]
    print(f"Number of LBP features: {len(feature_cols)}")


if __name__ == "__main__":
    main()