 Project Title

This project performs a comprehensive analysis on our dataset using multiple approaches:

- **Exploratory Data Analysis (EDA):** Conducted on the full dataset.
- **XGBoost:** Applied on the full dataset for classification/prediction.
- **Isolation Forest:** Utilized on a 1-million-row subset for anomaly detection.

## Overview

Our analysis leverages a variety of methods to uncover insights and build predictive models:

- **EDA:** Provides an in-depth look at the data distribution, patterns, and potential issues.
- **XGBoost:** A powerful gradient boosting framework used for classification tasks on the entire dataset.
- **Isolation Forest:** An unsupervised learning algorithm, applied to a subset of the data, to identify anomalies effectively.

## Data

- The dataset contains transaction records along with several features used for analysis.
- Detailed feature descriptions and data pre-processing steps are documented in the associated scripts.

## Methodology

### Exploratory Data Analysis (EDA)
- **Scope:** Full dataset
- **Objectives:**
  - Visualize and summarize data distributions.
  - Identify trends, correlations, and potential outliers.
  - Pre-process data for modeling.
- **Tools:** Pandas, Matplotlib, Seaborn

### XGBoost
- **Scope:** Full dataset
- **Objective:** Develop a robust classification model.
- **Highlights:**
  - Handles missing values and non-linear relationships effectively.
  - Hyperparameter tuning for optimal performance.
- **Tools:** XGBoost library, Scikit-Learn

### Isolation Forest
- **Scope:** 1 million rows subset
- **Objective:** Detect anomalies within the dataset.
- **Highlights:**
  - Efficient for large datasets where computational constraints exist.
  - Identifies outliers that could affect overall model performance.
- **Tools:** Scikit-Learn
