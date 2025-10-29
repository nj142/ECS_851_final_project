# 🧊 Using Machine Learning to Investigate Global Freeze-Up of Lake Ice

**Team Members:** Noah Jacobs  
**Semester:** Fall 2025  
**Instructor:** Dr. Johnny Ryan  
**Institution:** Duke University 

---

## 🌐 Project Summary
When studying ice cover dynamics on lakes and ponds in cold climates, determining freeze-up dates is challenging—especially at high latitudes due to low sun angles and frequent cloud cover during the freeze-up season.  
This project applies **machine learning techniques** to detect and analyze **lake freeze-up timing** globally using Sentinel-2 imagery.  
The repository includes a reproducible Jupyter-based workflow for classifying freeze-up stages within 50×50 km grid cells containing high-resolution lake masks. The workflow outputs lake-specific time series of ice cover, integrating validation datasets, rapid GEE preprocessing, and temporal analysis.

---

## 🎯 Problem Statement and Objectives
Accurate monitoring of lake freeze-up at global scales is critical for understanding hydrological and climatic processes across the cryosphere. However, remote sensing detection of lake ice is hindered by **low solar angles**, **persistent cloud cover**, and **limited satellite revisit rates** especially at high latitudes.

**Objectives / Expected Outcomes:**
1. Develop and evaluate multiple machine learning models (e.g., **Random Forest**, **Semantic Segmentation CNN**) for detecting lake ice cover from Sentinel-2 imagery.  
2. Quantify model accuracy in identifying freeze-up timing across diverse climatic and latitudinal zones.  
3. Implement the best-performing model into an **interactive Jupyter Notebook** to automate classification and time series generation for randomly selected global grid cells.  
4. Compare regional patterns of freeze-up timing to Arctic Oscillation (AO) and ENSO indices for large-scale climate analysis.

---

## 🧩 Planned Methods / Approach

Step 0. **Data Collection and Preprocessing**
   - Extract 50×50 km grid cells globally across a Mollweide equal area projection and clip **lake masks** from the Prior Lake Database (PLD) for a stratified sample of 50x50km cells across multiple biomes and latitudes.
   - Use the Labelbox workflow from my PhD repository to expand PLD for lakes within these cells into masks including all lakes as small as 0.001km^2.
   - Import the lake masks into GEE

Step 1. **Label Generation and Training Data**
   - Use the Classify notebook in this repository to classify whole Sentinel-2 images as either "all lakes ice covered" "some lakes ice covered" or "all lakes open water."  This will automatically create a training dataset for ice cover pixels without the need to manually delineate small ice formations in partially covered lakes.

Step 2. **Model Development**
   - Implement:
     - **Random Forest classifier** (scikit-learn) for initial baseline.
     - **U-Net style CNN** (TensorFlow/Keras) for spatially-aware segmentation.
   - Tune hyperparameters using grid search and cross-validation.

Step 3. **Model Evaluation**
   - Manually delineate first full open water image and last full ice image, and assess accuracy based on median estimated date between those two dates.
   - Identify the **best model** across regions to apply to a global scale.

Step 4. **Freeze-Up Time Series Generation**
   - Apply the selected model to multi-temporal imagery.
   - Extract per-lake freeze-up date (defined as first persistent ice detection).
   - Visualize and export results as **time series CSVs** of ice cover.

---

## 🌍 Datasets

| Dataset | Description | Source / Link |
|----------|--------------|----------------|
| **Prior Lake Database (PLD)** | High-resolution global lake mask dataset supplemented with small lakes (≥0.001 km²) | [Wang et al. 2025, Water Resources Research](https://doi.org/10.1029/2023WR036896) |
| **Sentinel-2 SR Imagery (2017–2025)** | Multispectral imagery used for ice classification | Google Earth Engine (`COPERNICUS/S2_SR`) |
| **Labelbox Annotations** | Manual delineations used to supplement lake masks | Generated from prior PhD repositoryby Noah Jacobs |

---

## 🧠 Python Packages Required

```python
pandas
numpy
matplotlib
scikit-learn
tensorflow
geopandas
rasterio
earthengine-api
folium
seaborn
datetime
glob
os
```
