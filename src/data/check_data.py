from pathlib import Path

import numpy as np
import pandas as pd
import tifffile as tiff
from tqdm import tqdm


PROJECT_ROOT = Path(__file__).resolve().parents[1]

PHASE_DIR = PROJECT_ROOT / "data" / "DemodulatedImages" / "PhaseDifference"
LABEL_CSV = PROJECT_ROOT / "data" / "labels.csv"
OUT_DIR = PROJECT_ROOT / "results" / "metrics"


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    files = sorted(
        list(PHASE_DIR.rglob("*.tif")) +
        list(PHASE_DIR.rglob("*.tiff"))
    )

    print(f"Phase directory: {PHASE_DIR}")
    print(f"Total phase difference images: {len(files)}")

    if len(files) == 0:
        print("No .tif or .tiff files found. Check your folder path.")
        return

    records = []

    for f in tqdm(files):
        img = tiff.imread(f)

        records.append({
            "filename": f.name,
            "relative_path": str(f.relative_to(PROJECT_ROOT)),
            "shape": str(img.shape),
            "dtype": str(img.dtype),
            "min": float(np.min(img)),
            "max": float(np.max(img)),
            "mean": float(np.mean(img)),
            "std": float(np.std(img)),
            "nan_count": int(np.isnan(img).sum()) if np.issubdtype(img.dtype, np.floating) else 0,
        })

    image_df = pd.DataFrame(records)

    print("\nImage shape counts:")
    print(image_df["shape"].value_counts())

    print("\nDtype counts:")
    print(image_df["dtype"].value_counts())

    print("\nValue range summary:")
    print(image_df[["min", "max", "mean", "std", "nan_count"]].describe())

    out_file = OUT_DIR / "phase_image_summary.csv"
    image_df.to_csv(out_file, index=False)
    print(f"\nSaved image summary to: {out_file}")

    if not LABEL_CSV.exists():
        print("\nlabels.csv not found. Run src/create_labels.py first.")
        return

    labels = pd.read_csv(LABEL_CSV)

    print("\nLabels preview:")
    print(labels.head())

    print("\nLabel file shape:")
    print(labels.shape)

    print("\nSeverity counts:")
    print(labels["severity"].value_counts())

    print("\nBinary label counts:")
    print(labels["binary_name"].value_counts())

    image_paths = set(image_df["relative_path"])
    label_paths = set(labels["relative_path"])

    missing_labels = image_paths - label_paths
    missing_images = label_paths - image_paths

    print("\nImage-label matching check:")

    if not missing_labels and not missing_images:
        print("All image files match labels.csv.")
    else:
        print(f"Images without labels: {len(missing_labels)}")
        print(f"Labels without images: {len(missing_images)}")

        if missing_labels:
            print("\nExample images without labels:")
            print(list(missing_labels)[:10])

        if missing_images:
            print("\nExample labels without images:")
            print(list(missing_images)[:10])


if __name__ == "__main__":
    main()