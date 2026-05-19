# MATLAB Feature Extraction

This folder contains MATLAB scripts for handcrafted feature extraction.

The main features are extracted using the Balu toolbox:

- LBP
- BSIF
- HOG

Before running the scripts, add the Balu toolbox and BSIF filter banks to the MATLAB path.

Example feature settings used in the final experiments:

- LBP59
- BSIF 5×5 7-bit
- BSIF 7×7 8-bit
- BSIF 9×9 10-bit

The extracted features are then evaluated in Python using RLDA.