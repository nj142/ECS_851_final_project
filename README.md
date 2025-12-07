<img width="2941" height="3571" alt="YKD_footprints_summary" src="https://github.com/user-attachments/assets/79f01f1b-dac1-4652-99a9-3fd8daeb7abd" /># Using Machine Learning to Investigate Global Freeze-Up of Lake Ice

**Team Members:** Noah Jacobs  
**Semester:** Fall 2025  
**Instructor:** Dr. Johnny Ryan  
**Institution:** Duke University 

<img width="1317" height="650" alt="image" src="https://github.com/user-attachments/assets/cb51df73-55c8-4a5c-b40c-081c30fa834f" />

---

## Project Summary

This project applies **machine learning techniques** to detect and analyze **lake freeze-up timing** globally using Sentinel-2 imagery. The repository includes a reproducible Jupyter-based workflow for classifying freeze-up stages within 50×50 km grid cells containing high-resolution lake masks. 

---

## Problem Statement and Objectives
Accurate monitoring of lake freeze-up at global scales is critical for understanding hydrological and climatic processes across the cryosphere. However, remote sensing detection of lake ice is hindered by **low solar angles**, **persistent cloud cover**, and **limited satellite revisit rates** especially at high latitudes.

**Objectives / Expected Outcomes:**

1. Develop and evaluate a machine learning model (**Random Forest**) for detecting lake ice cover from Sentinel-2 imagery.  

2. Quantify model accuracy in identifying freeze-up timing across diverse climatic and latitudinal zones.  

3. Implement the best-performing model frond from GridSearchCV hyperparameter tuning into an **interactive Jupyter Notebook** to automate classification and time series generation for selected study site cells.  

---

## Methods

Step 0. **Data Collection and Preprocessing**
   - Select 50×50 km grid cells from an equal area projection (e.g. Alaska Albers or Mollweide)
   - Use the Labelbox workflow from my PhD repository to expand the PLD dataset for lakes within these cells into masks including all lakes as small as 0.001km^2.

Step 1. **Label Generation and Training Data**
   - Classify all Sentinel-2 and Planet images as either "all lakes ice covered" "some lakes ice covered" or "all lakes open water."  This will automatically create a training dataset for ice cover pixels without the need to manually delineate small ice formations in partially covered lakes.

Step 2. **Model Development**
   - Implement **Random Forest classifier** (scikit-learn)
   - Tune hyperparameters using grid search and cross-validation.

Step 3. **Model Evaluation**
   - Assess accuracy based on test dataset
   - Identify the **best model** across regions to apply to a global scale for further analysis

Step 4. **Freeze-Up Time Series Generation (Incomplete)**
   - Apply the selected model to multi-temporal imagery.
   - Extract per-lake freeze-up date (defined as first persistent ice detection).
   - Visualize and export results as **time series CSVs** of ice cover.

---

## Datasets

| Dataset | Description | Source / Link |
|----------|--------------|----------------|
| **Prior Lake Database (PLD)** | High-resolution global lake mask dataset supplemented with small lakes (≥0.001 km²) | [Wang et al. 2025, Water Resources Research](https://doi.org/10.1029/2023WR036896) |
| **Sentinel-2 SR Imagery (2017–2025)** | Multispectral imagery used for ice classification | AWS STAC API |
| **Labelbox Annotations** | Manual delineations used to supplement lake masks | Generated from prior PhD repositoryby Noah Jacobs |
| **ALPOD Lake Masks for Alaska** | Alaska-specific high resolution lake masks created by Eric Levenson | [Levenson et al. 2025, Geophysical Research Letters](https://doi.org/10.1029/2024GL112771) |

---

## Python Packages

```python
pandas
cv2
numpy
matplotlib & pyplot
pyarrow & parquet
scikit-learn
joblib
tensorflow
geopandas
rasterio
shapely
tqdm
numba
earthengine-api
folium
pathlib
shutil
datetime
glob
os
```
