from pathlib import Path

import numpy as np
import pandas as pd

from sklearn.model_selection import StratifiedShuffleSplit, StratifiedKFold, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report


PROJECT_ROOT = Path(__file__).resolve().parents[1]

FEATURE_FILES = {
    "bsif_9x9_10bit_nocrop": PROJECT_ROOT / "data" / "processed" / "bsif_bits_sweep_nocrop" / "balu_bsif_9x9_10bit_nocrop.csv",
    "lbp59_nocrop": PROJECT_ROOT / "data" / "processed" / "balu_nocrop" / "balu_lbp59_nocrop.csv",
    "lbp59_bsif_9x9_10bit_nocrop": PROJECT_ROOT / "data" / "processed" / "final_features" / "balu_lbp59_bsif_9x9_10bit_nocrop.csv",
}

OUT_DIR = PROJECT_ROOT / "results" / "metrics"
OUT_FILE = OUT_DIR / "final_best_features_rlda_summary.csv"

META_COLS = {
    "filename",
    "relative_path",
    "sample_id",
    "severity",
    "binary_label",
    "binary_name",
}


def run_one(name: str, file_path: Path):
    print("\n" + "=" * 80)
    print(f"Training feature set: {name}")
    print(f"File: {file_path}")

    df = pd.read_csv(file_path)

    feature_cols = [c for c in df.columns if c not in META_COLS]

    X = df[feature_cols].values.astype(np.float64)
    y = df["binary_label"].values.astype(int)

    print(f"X shape: {X.shape}")
    print(f"Class counts: {np.bincount(y)}")

    splitter = StratifiedShuffleSplit(
        n_splits=50,
        test_size=0.35,
        random_state=42,
    )

    shrinkage_grid = np.linspace(0.04, 0.16, 25)

    records = []

    last_y_test = None
    last_y_pred = None

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

        records.append({
            "feature_set": name,
            "rep": rep,
            "accuracy": acc,
            "best_shrinkage": grid.best_params_["clf__shrinkage"],
        })

        last_y_test = y_test
        last_y_pred = y_pred

        print(
            f"Rep {rep:02d} | "
            f"acc={acc:.4f} | "
            f"best_shrinkage={grid.best_params_['clf__shrinkage']:.2f}"
        )

    result_df = pd.DataFrame(records)

    print("\nResult:")
    print(f"Mean accuracy: {result_df['accuracy'].mean():.4f}")
    print(f"Std accuracy : {result_df['accuracy'].std():.4f}")
    print(f"Min accuracy : {result_df['accuracy'].min():.4f}")
    print(f"Max accuracy : {result_df['accuracy'].max():.4f}")

    print("\nLast split confusion matrix:")
    print(confusion_matrix(last_y_test, last_y_pred))

    print("\nLast split classification report:")
    print(classification_report(
        last_y_test,
        last_y_pred,
        target_names=["Normal", "Defective"],
    ))

    return result_df


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    all_results = []

    for name, path in FEATURE_FILES.items():
        if not path.exists():
            print(f"Missing file: {path}")
            continue

        result_df = run_one(name, path)
        all_results.append(result_df)

    all_results = pd.concat(all_results, ignore_index=True)

    summary = (
        all_results
        .groupby("feature_set")["accuracy"]
        .agg(["mean", "std", "min", "max"])
        .reset_index()
        .sort_values("mean", ascending=False)
    )

    all_results.to_csv(OUT_DIR / "final_best_features_all_results.csv", index=False)
    summary.to_csv(OUT_FILE, index=False)

    print("\n" + "=" * 80)
    print("Final summary:")
    print(summary)

    print(f"\nSaved summary to: {OUT_FILE}")


if __name__ == "__main__":
    main()