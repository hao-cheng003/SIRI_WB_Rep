from pathlib import Path

import pandas as pd
import tifffile as tiff
import matplotlib.pyplot as plt


PROJECT_ROOT = Path(__file__).resolve().parents[1]
LABEL_CSV = PROJECT_ROOT / "data" / "labels.csv"
OUT_DIR = PROJECT_ROOT / "results" / "figures"


def load_image(relative_path: str):
    img_path = PROJECT_ROOT / relative_path
    return tiff.imread(img_path)


def plot_group(labels, group_name, n=6):
    subset = labels[labels["binary_name"] == group_name].head(n)

    fig, axes = plt.subplots(1, n, figsize=(3 * n, 4))

    for ax, (_, row) in zip(axes, subset.iterrows()):
        img = load_image(row["relative_path"])

        ax.imshow(img, cmap="jet")
        ax.set_title(row["sample_id"], fontsize=8)
        ax.axis("off")

    plt.tight_layout()

    out_path = OUT_DIR / f"{group_name.lower()}_examples.png"
    plt.savefig(out_path, dpi=200)
    plt.close()

    print(f"Saved: {out_path}")


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    labels = pd.read_csv(LABEL_CSV)

    plot_group(labels, "Normal", n=6)
    plot_group(labels, "Defective", n=6)


if __name__ == "__main__":
    main()