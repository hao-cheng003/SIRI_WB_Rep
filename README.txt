# README

SIRI_PoultryWB
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

## (RawPatternImages)

## Dataset Structure
    When extracting the raw data (phase-shifted pattern) from the "SIRI_PoultryWB.7z" archive, the dataset contains two main directories:

    1. **Normal**: Contains 72 WB-free samples.
    2. **Defective**: Contains 96 WB-affected samples, including:
        - 39 samples with Moderate-Degree severity.
        - 57 samples with Severe-Degree severity.

    The samples with severe and moderate WB were combined to form the “Defective” group, although the two subcategories can be treated separately in the reuse of the dataset for model development.

## Directory Organization
    Within these directories, the dataset is further organized into multiple subfolders. For example:

    - `Batch01_Normal_S005`
    - `Batch01_Defective_S010`

    Each subfolder contains a collection of 24 grayscale SIRI pattern images in the .tif format, each of size 2048×2048 pixels with a depth of 16 bits per pixel. 
    These images are obtained using SIRI techniques under the illumination of three phase-shifted sinusoidal patterns at eight distinct spatial frequencies, resulting in 24 pattern images acquired from each sample.

## Dataset Summary
    - Total samples: 168
    - Total images: 4,032
    - Storage space required: Approximately 32 GB

## File Naming Convention
    The file naming convention for each file in the dataset is descriptive and systematic to provide information about each image's characteristics. Each file name includes three key elements:

    1. **Sample Type**: "Broiler"
    2. **Spatial Frequency**: "015Hz", "022Hz", "030Hz", "040Hz", "055Hz", "070Hz", "090Hz", "150Hz" (e.g., "015Hz" for 0.015 cycles/mm)
    3. **Phase Shift**: "PS1", "PS2", "PS3" (e.g., "PS1" for the first phase shift)

### Examples
    - `Broiler_015Hz_PS1.tif`: Image obtained using the first phase-shifted illumination pattern at a spatial frequency of 0.015 cycles/mm.
    - `Broiler_150Hz_PS3.tif`: Image captured using the third phase-shifted illumination pattern at 0.150 cycles/mm.

The consistent file naming structure helps to easily identify and organize images based on their imaging conditions, thereby facilitating the processing and analysis of data.

-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
## (DemodulatedImages)

## Dataset Structure
    The "DemodulatedImages" dataset simplifies access to demodulated images for individuals who may lack expertise in the demodulation process. It contains:

    1. IntensityDCAC:
        The "IntensityDCAC" folder is divided into subfolders based on spatial frequencies (AC), along with a DC subfolder. Inside of each subfolder:

        **1Normal:** 72 WB-free samples.
        **2Defective:** 96 WB-affected samples, including:
            - 39 samples with Moderate-Degree severity.
            - 57 samples with Severe-Degree severity.

        Each folder structure is consistent across all spatial frequency categories.
        For convenience, Moderate-Degree and Severe-Degree WB samples are grouped under the 1Defective category, but subcategories can be treated separately for flexibility in dataset reuse.

    2. PhaseDifference:
        The "PhaseDifference" folder has a simpler structure with two subfolders: "1Normal" and "2Defective."

        **1Normal:** 72 WB-free samples.
        **2Defective:** 96 WB-affected samples (both Moderate-Degree and Severe-Degree WB).

## Each image in these directories:
    - Format: .tif file
    - Resolution: 1024×1024 pixels

## Dataset Summary
    - Total images: 1,680
    - Storage space required: ~1.64 GB

## File Naming Convention
    File names are descriptive and systematic, providing details about each image's properties, making navigation and analysis straightforward.