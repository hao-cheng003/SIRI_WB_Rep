# Reproduction of Woody Breast Classification Using SIRI and Surface Profilometry

This repository contains a reproduction of the main classification pipeline from the paper:

**Assessment of woody breast in broiler breast fillets using structured-illumination reflectance imaging coupled with surface profilometry**
https://www.sciencedirect.com/science/article/pii/S0260877424005259

The goal of this project is to reproduce the paper's phase-difference-image-based woody breast classification method using handcrafted texture features and a regularized linear discriminant analysis classifier.

## Project Overview

Woody breast is a muscle abnormality in broiler breast fillets. The original paper used structured-illumination reflectance imaging (SIRI) and surface profilometry to classify normal and defective chicken breast samples.

In this reproduction, I focused on the phase difference images provided in the dataset. Instead of rebuilding the full structured-light demodulation pipeline from raw pattern images, I used the provided demodulated phase difference images directly.

The main reproduced pipeline is:

1. Load phase difference `.tif` images.
2. Extract texture features using LBP and BSIF.
3. Train and evaluate an RLDA classifier.
4. Use 65/35 repeated holdout validation with 50 repetitions.
5. Compare the reproduced results with the original paper.

## Dataset

The dataset contains demodulated phase difference images of broiler breast fillets.

The data used in this project is organized as:

```text
data/
└── DemodulatedImages/
    └── PhaseDifference/
        ├── 1Normal/
        └── 2Defective/
```

The dataset used in this reproduction contains:

| Class | Number of Samples |
|---|---:|
| Normal | 72 |
| Defective | 96 |
| Total | 168 |

All phase difference images are `.tif` files with size `1024 × 1024`.

The original dataset is not included in this repository. Please download it from the official data source and place it under the directory structure shown above.

## Method

### Feature Extraction

Two main texture descriptors were tested:

- Local Binary Pattern (LBP)
- Binarized Statistical Image Features (BSIF)

The final feature extraction was performed using the MATLAB Balu toolbox, because the original paper also used MATLAB-based handcrafted feature extraction.

The tested feature sets include:

- Python LBP 59-bin
- Balu LBP59
- Balu BSIF 5×5 7-bit
- Balu BSIF 7×7 8-bit
- Balu BSIF 9×9 10-bit
- Balu LBP59 + BSIF 9×9 10-bit

### Classifier

The classifier used in this project is:

- Regularized Linear Discriminant Analysis (RLDA)

The shrinkage parameter was selected using cross-validation on the training set.

### Evaluation Protocol

The evaluation protocol follows the original paper as closely as possible:

- 65% training / 35% testing split
- 50 repeated holdout trials
- 10-fold cross-validation on the training set for shrinkage selection
- Mean accuracy and standard deviation are reported

## Final Results

| Feature Set | Preprocessing | Classifier | Mean Accuracy | Std |
|---|---|---|---:|---:|
| Python LBP 59-bin | no-crop | RLDA | 83.90% | - |
| Balu LBP59 | no-crop | RLDA | 87.49% | - |
| Balu BSIF 5×5 7-bit | no-crop | RLDA | 87.83% | - |
| Balu BSIF 7×7 8-bit | no-crop | RLDA | 88.78% | - |
| Balu BSIF 9×9 10-bit | no-crop | RLDA | **90.85%** | **3.64%** |
| Balu LBP59 + BSIF 9×9 10-bit | no-crop | RLDA | 90.78%–90.98% | ≈3.4% |

The best stable reproduced result was obtained using:

```text
Balu BSIF 9×9 10-bit no-crop + RLDA
```

with an average accuracy of approximately **90.85%**.

## Comparison with the Original Paper

The original paper reported approximately **92.95%** overall accuracy using phase difference images with LBP + optimized BSIF features and RLDA.

Our best reproduced result reached approximately **90.85%** average accuracy.

Although the reproduced accuracy is slightly lower than the reported result, the main experimental trend is consistent with the paper:

- Phase difference images are useful for woody breast classification.
- Balu-based handcrafted texture features perform better than simple Python LBP features.
- BSIF performs better than LBP alone.
- Optimizing BSIF parameters improves the classification result.
- Combining LBP and BSIF produced comparable performance, but did not consistently outperform BSIF alone in this reproduction.

The remaining gap may come from differences in ROI preprocessing, feature extraction details, BSIF implementation, histogram normalization, and the randomness caused by the small dataset size.

## Repository Structure

```text
SIRI_WB_Rep/
├── data/
│   └── README.md
├── features/
│   └── README.md
├── matlab/
│   ├── extract_lbp.m
│   ├── extract_bsif.m
│   ├── extract_hog.m
│   └── README.md
├── src/
│   ├── check_dataset.py
│   ├── run_rlda_eval.py
│   ├── run_bsif_search.py
│   └── make_result_table.py
│   └── archive
│       └── train_lbp59_crop_rlda.py
├── results/
│   ├── final_results.csv
│   ├── final_result_table.md
│   └── accuracy_bar_chart.png
├── report/
│   └── reproduction_report.pdf
├── requirements.txt
├── environment.yml
└── README.md
```

## How to Run

### 1. Prepare the Python Environment

Create the conda environment:

```bash
conda env create -f environment.yml
conda activate siri_wb
```

Or install dependencies manually:

```bash
pip install -r requirements.txt
```

### 2. Prepare the Dataset

Place the phase difference images under:

```text
data/DemodulatedImages/PhaseDifference/1Normal/
data/DemodulatedImages/PhaseDifference/2Defective/
```

Then run:

```bash
python scripts/check_dataset.py
```

This script checks the number of images, image size, data type, and label consistency.

### 3. Extract Features

Feature extraction was mainly performed in MATLAB using the Balu toolbox.

Example MATLAB scripts are located in:

```text
matlab/
```

Before running the scripts, make sure the Balu toolbox and BSIF filter banks are correctly added to the MATLAB path.

### 4. Run RLDA Evaluation

After feature extraction, run:

```bash
python scripts/run_rlda_eval.py
```

This performs repeated holdout evaluation using RLDA.

### 5. Generate Final Result Table

```bash
python scripts/make_result_table.py
```

The final results will be saved under:

```text
results/
```

## Notes

This project does not aim to claim a new state-of-the-art result. The goal is to reproduce and analyze the main pipeline of the original paper.

The reproduced result is close to the reported result, but not identical. This is expected because some implementation details in preprocessing, ROI selection, and feature extraction are not fully specified in the paper.

## Main Conclusion

This reproduction reached approximately **90.85%** average classification accuracy using phase difference images, BSIF 9×9 10-bit features, and RLDA.

The result is slightly lower than the original paper's reported **92.95%**, but the main conclusion is consistent: phase difference images combined with BSIF-based texture features are effective for woody breast classification.