from pathlib import Path
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]

PHASE_DIR = PROJECT_ROOT / "data" / "DemodulatedImages" / "PhaseDifference"
OUT_FILE = PROJECT_ROOT / "data" / "labels.csv"


def parse_label_from_path(file_path: Path):

    parts_lower = [p.lower() for p in file_path.parts]

    if "1normal" in parts_lower:
        severity = "Normal"
        binary_label = 0
        binary_name = "Normal"

    elif "2defective" in parts_lower:
        binary_label = 1
        binary_name = "Defective"

        name_lower = file_path.stem.lower()

        if "moderate" in name_lower:
            severity = "Moderate"
        elif "severe" in name_lower:
            severity = "Severe"
        else:
            severity = "Defective"

    else:
        raise ValueError(f"Cannot parse label from path: {file_path}")

    return severity, binary_label, binary_name


def main():
    files = sorted(
        list(PHASE_DIR.rglob("*.tif")) +
        list(PHASE_DIR.rglob("*.tiff"))
    )

    print(f"Phase directory: {PHASE_DIR}")
    print(f"Found image files: {len(files)}")

    if len(files) == 0:
        print("No .tif or .tiff files found.")
        return

    records = []
    failed_files = []

    for f in files:
        try:
            severity, binary_label, binary_name = parse_label_from_path(f)

            records.append({
                "filename": f.name,
                "relative_path": str(f.relative_to(PROJECT_ROOT)),
                "sample_id": f.stem,
                "severity": severity,
                "binary_label": binary_label,
                "binary_name": binary_name,
            })

        except ValueError:
            failed_files.append(str(f))

    if failed_files:
        print("\nThese files could not be parsed:")
        for name in failed_files:
            print(name)
        return

    df = pd.DataFrame(records)
    df.to_csv(OUT_FILE, index=False)

    print(f"\nSaved labels to: {OUT_FILE}")

    print("\nTotal samples:")
    print(len(df))

    print("\nSeverity counts:")
    print(df["severity"].value_counts())

    print("\nBinary label counts:")
    print(df["binary_name"].value_counts())


if __name__ == "__main__":
    main()