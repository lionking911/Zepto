# Titanic Modeling Workflow

This document explains the training workflow implemented in `Analytics/modeling.py` and how to use the resulting model pipeline.

## Overview

The script builds and compares several machine learning models for the Titanic dataset and produces evaluation metrics, visualizations, and a saved model artifact. It covers:

- Logistic Regression
- Decision Tree Classifier
- Random Forest Classifier
- Class imbalance handling
- Hyperparameter tuning with `GridSearchCV`
- Linear Regression for predicting `fare`
- End-to-end model persistence with `joblib`

## Dataset

The script reads:

- `cleaned_titanic.csv`

It expects the dataset to contain columns such as:

- `pclass`
- `sex`
- `age`
- `sibsp`
- `parch`
- `fare`
- `embarked`
- `survived`

## Target and Features

For classification, the script defines:

- Features: `['pclass', 'sex', 'age', 'sibsp', 'parch', 'fare', 'embarked']`
- Target: `survived`

The script uses a stratified train/test split to preserve the class ratio:

- `test_size=0.2`
- `stratify=y`
- `random_state=42`

## Data Preprocessing

The script uses a `ColumnTransformer` with separate pipelines for numeric and categorical variables.

### Numeric features

- `['age', 'fare', 'sibsp', 'parch']`
- `SimpleImputer(strategy='mean')`
- `StandardScaler()`

### Categorical features

- `['pclass', 'sex', 'embarked']`
- `SimpleImputer(strategy='most_frequent')`
- `OneHotEncoder(handle_unknown='ignore', drop='first')`

This ensures that both numerical and categorical variables are processed consistently before model training.

## Models Evaluated

### 1. Logistic Regression

The script fits a baseline logistic regression pipeline:

- Preprocessor
- `LogisticRegression(max_iter=1000)`

It reports:

- Accuracy
- Precision
- Recall
- F1 Score
- ROC AUC
- Classification report
- Confusion matrix
- ROC curve

### 2. Decision Tree Classifier

A second pipeline is created with:

- `DecisionTreeClassifier(max_depth=5, random_state=42)`

This model also prints the same classification metrics and visualizations.

It also generates a decision tree visualization using `plot_tree`, with encoded feature names cleaned up for readability.

### 3. Random Forest Classifier

The script tests:

- `RandomForestClassifier(n_estimators=100, random_state=42, max_depth=6)`

This model is evaluated with the same metrics and ROC plot.

## Model Comparison Table

The script stores results in `comparision_list` and prints a table using `tabulate`, including:

- Model name
- Accuracy
- Precision
- Recall
- F1 score
- ROC-AUC
- Confusion matrix

## Imbalance Handling

The script includes an imbalance analysis and three alternatives:

1. Baseline model without any class balancing
2. `LogisticRegression(class_weight='balanced')`
3. `SMOTE` applied only on the training fold

It reports the precision, recall, F1-score, and support for the positive class (`survived`).

## Hyperparameter Tuning

The script uses `GridSearchCV` for a Random Forest model with:

- `n_estimators`: `[1000]`
- `max_depth`: `[5, 10, None]`
- `max_features`: `['sqrt', 'log2']`

It prints the best parameter set and the corresponding out-of-bag (OOB) score.

## Linear Regression Section

The script then switches from binary classification to regression by predicting `fare`.

### Target

- `target = 'fare'`

### Regression features

- `['pclass', 'sex', 'age', 'sibsp', 'parch', 'embarked']`

### Regression model

- `LinearRegression()`

### Metrics reported

- Mean Absolute Error (MAE)
- Root Mean Squared Error (RMSE)
- R²
- Adjusted R²

It also creates a residual plot to inspect model fit and heteroscedasticity.

## Final Pipeline and Persistence

At the end of the script, it creates a full pipeline:

- Preprocessing
- Random Forest classifier

Then it saves the trained model as:

- `full_prediction_pipeline.joblib`

This allows the script to reload the model and predict directly on raw input data without manually preprocessing the features.

Example:

```python
loaded_pipeline = joblib.load("full_prediction_pipeline.joblib")
predictions = loaded_pipeline.predict(new_raw_input)
probabilities = loaded_pipeline.predict_proba(new_raw_input)[:, 1]
```

## How to Run

From the project root, run:

```bash
python Analytics/modeling.py
```

Make sure the dataset file `cleaned_titanic.csv` is available in the working directory or update the file path in the script accordingly.

## Dependencies

The script requires:

- pandas
- numpy
- matplotlib
- seaborn
- scikit-learn
- imbalanced-learn
- tabulate
- joblib

Install them with:

```bash
pip install pandas numpy matplotlib seaborn scikit-learn imbalanced-learn tabulate joblib
```

## Key Notes

- The script is a full experimental notebook-like workflow, not a clean production-ready API.
- Some variable names are informal (for example, `comparision_list`) and could be cleaned up.
- The script repeatedly reuses and redefines variables across sections, which is fine for experimentation but not ideal for maintainability.
- For production use, it would be better to separate the workflow into:
  - data loading
  - preprocessing
  - model training
  - evaluation
  - save/load functions
  - CLI entry point

## Suggested Improvements

- Split the code into reusable functions
- Save metrics to a CSV/JSON report
- Add a command-line interface for model selection
- Version the model artifact and schema
- Add unit tests for preprocessing steps
- Standardize naming conventions and variable spelling

## Summary

This script is a comprehensive exploratory modeling workflow for Titanic survival prediction, including preprocessing, model comparison, class imbalance handling, tuning, regression analysis, visual evaluation, and artifact export.

It is useful for learning and experimentation, and with a little refactoring it can be turned into a reusable pipeline for real projects.

