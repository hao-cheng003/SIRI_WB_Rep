from pathlib import Path

import numpy as np
import pandas as pd

from sklearn.model_selection import StratifiedShuffleSplit, StratifiedKFold, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.metrics import accuracy_score


PROJECT_ROOT = Path(__file__).resolve().parents[1]

FEATURE_DIR = PROJECT_ROOT / "data" / "processed" / "bsif_bits_sweep_nocrop"
OUT_DIR = PROJECT_ROOT / "results" / "metrics"
OUT_FILE = OUT_DIR / "bsif_bits_sweep_nocrop_rlda_summary.csv"

META_COLS = {
    "filename",
    "relative_path",
    "sample_id",
    "severity",
    "binary_label",
    "binary_name",
}


def train_one(feature_file: Path) -> dict:
    df = pd.read_csv(feature_file)

    feature_cols = [c for c in df.columns if c not in META_COLS]

    X = df[feature_cols].values.astype(np.float64)
    y = df["binary_label"].values.astype(int)

    splitter = StratifiedShuffleSplit(
        n_splits=50,
        test_size=0.35,
        random_state=42,
    )

    shrinkage_grid = np.linspace(0.0, 0.5, 11)

    accuracies = []
    best_shrinkages = []

    print("\n" + "=" * 80)
    print(f"Training: {feature_file.name}")
    print(f"X shape: {X.shape}")
    print(f"Class counts: {np.bincount(y)}")

    for rep, (train_idx, test_idx) in enumerate(splitter.split(X, y), start=1):
        X_train, X_test = X[train_idx], X[test_idx]
        y_train, y_test = y[train_idx], y[test_idx]

        pipe = Pipeline([
            ("scaler", StandardScaler()),
            ("clf", LinearDiscriminantAnalysis(solver="lsqr")),
        ])

        cv = StratifiedKFold(
            n_splits=10,
            shuffle=True,
            random_state=rep,
        )

        grid = GridSearchCV(
            estimator=pipe,
            param_grid={"clf__shrinkage": shrinkage_grid},
            cv=cv,
            scoring="accuracy",
            n_jobs=-1,
        )

        grid.fit(X_train, y_train)

        y_pred = grid.predict(X_test)
        acc = accuracy_score(y_test, y_pred)

        accuracies.append(acc)
        best_shrinkages.append(grid.best_params_["clf__shrinkage"])

        print(
            f"Rep {rep:02d} | "
            f"acc={acc:.4f} | "
            f"best_shrinkage={grid.best_params_['clf__shrinkage']:.2f}"
        )

    result = {
        "feature_file": feature_file.name,
        "mean": float(np.mean(accuracies)),
        "std": float(np.std(accuracies, ddof=1)),
        "min": float(np.min(accuracies)),
        "max": float(np.max(accuracies)),
        "median_best_shrinkage": float(np.median(best_shrinkages)),
    }

    print("\nResult:")
    print(f"Mean accuracy: {result['mean']:.4f}")
    print(f"Std accuracy : {result['std']:.4f}")
    print(f"Min accuracy : {result['min']:.4f}")
    print(f"Max accuracy : {result['max']:.4f}")
    print(f"Median shrinkage: {result['median_best_shrinkage']:.3f}")

    return result


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    if not FEATURE_DIR.exists():
        print(f"Feature directory does not exist: {FEATURE_DIR}")
        print("You need to run matlab/extract_bsif_bits_sweep_nocrop.m first.")
        return

    files = sorted([
        f for f in FEATURE_DIR.glob("*.csv")
        if "10bit" in f.name
    ])


    if not files:
        print(f"No 10bit csv files found in: {FEATURE_DIR}")
        return
    
    print("\nFiles to train:")
    for f in files:
        print(f"  - {f.name}")


    print(f"Feature directory: {FEATURE_DIR}")
    print(f"Found csv files: {len(files)}")

    print("\nFiles to train:")
    for f in files:
        print(f"  - {f.name}")

    results = []

    for f in files:
        results.append(train_one(f))

    summary = pd.DataFrame(results)
    summary = summary.sort_values("mean", ascending=False)

    summary.to_csv(OUT_FILE, index=False)

    print("\n" + "=" * 80)
    print("BSIF bits sweep summary:")
    print(summary)

    print(f"\nSaved summary to: {OUT_FILE}")


if __name__ == "__main__":
    main()