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
- 
============ Evaluate all three models  ============
+---------------------+------------+-------------+----------+------------+-----------+--------------------+
| Model               |   Accuracy |   Precision |   Recall |   F1 Score |   ROC-AUC | Confusion-Matrix   |
+=====================+============+=============+==========+============+===========+====================+
| Logistic Regression |   0.782051 |    0.75     | 0.703125 |   0.725806 |  0.844005 | [[77 15]           |
|                     |            |             |          |            |           |  [19 45]]          |
+---------------------+------------+-------------+----------+------------+-----------+--------------------+
| Decision Tree       |   0.801282 |    0.851064 | 0.625    |   0.720721 |  0.846977 | [[85  7]           |
|                     |            |             |          |            |           |  [24 40]]          |
+---------------------+------------+-------------+----------+------------+-----------+--------------------+
| Random Forest       |   0.814103 |    0.888889 | 0.625    |   0.733945 |  0.851053 | [[87  5]           |
|                     |            |             |          |            |           |  [24 40]]          |
+---------------------+------------+-------------+----------+------------+-----------+--------------------+
  Why Random Forest is the Best ChoiceHighest Overall Accuracy & ROC-AUC:
  It correctly predicts the data points 81.41% of the time. Its ROC-AUC (0.8510) is also the highest, proving that it has the strongest capability to distinguish between the two classes across various thresholds.Superior Precision (88.88%): This is the standout feature of this model. When Random Forest predicts a case as positive, it is correct nearly 89% of the time. Look at the Confusion Matrix: it only generated 5 False Positives (top-right of its matrix), whereas Logistic Regression generated 15.Best Balanced F1-Score (73.39%): Because it maintains a massive jump in Precision while keeping the same Recall as the Decision Tree, its harmonic mean (F1 Score) is the highest among all three.

  How ever what model to use depends on business need and requirments

  If your priority is high reliability and minimizing false alarms (False Positives), Random Forest is the undisputed winner.

## Imbalance Handling

The script includes an imbalance analysis and three alternatives:

1. Baseline model without any class balancing
2. `LogisticRegression(class_weight='balanced')`
3. `SMOTE` applied only on the training fold

It reports the precision, recall, F1-score, and support for the positive class (`survived`).
=== Performance Comparison (Target: Survived Class) ===
           Baseline (No Handling)  Class Weight Balanced  SMOTE (Train Fold Only)
Precision                   0.719                  0.702                    0.722
Recall                      0.667                  0.760                    0.729
F1-Score                    0.692                  0.730                    0.725

The Class Weight Balanced strategy worked best overall because it achieved the highest F1-Score (0.730) and Recall (0.760) for the minority class (Survived).

Why Class Weight Balanced WonOptimized the Trade-off (F1-Score): F1-Score is the harmonic mean of Precision and Recall. By scoring 0.730, Class Weight Balanced proved to be the most stable technique, providing the best mathematical balance between catching positive cases and staying accurate.Massive Recall Boost: It jumped the Recall from 0.667 to 0.760 (a ~14% improvement over Baseline). In survival datasets, Recall is usually the most critical metric because missing a "survived" instance (False Negative) is riskier than predicting someone survived when they did not (False Positive).Why it beat SMOTE: While SMOTE gave a slightly higher Precision (0.722 vs 0.702), it did so at the cost of Recall (0.729 vs 0.760). SMOTE creates synthetic data points which can sometimes blur the decision boundary if the classes overlap heavily. Class Weighting simply tells the algorithm to pay more attention to the existing minority samples, making it cleaner and more effective for this dataset structure.

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

It also creates a residual plot 
we state model fit has  heteroscedasticity.as the graph is like cone shape


============ model comparison table  ============
+---------------------+--------------------------------------------------------------+---------------------------------------------------+
|       Model Info      |                     Classification Metrics                     |                  Regression Metrics                 |
+---------------------+------------+-------------+----------+------------+-----------+--------------------+---------+---------+----------+---------------+
| Model               |   Accuracy |   Precision |   Recall |   F1 Score |   ROC-AUC | Confusion-Matrix   |     MAE |    RMSE |       R2 |   Adjusted R2 |
+=====================+============+=============+==========+============+===========+====================+=========+=========+==========+===============+
| Logistic Regression |   0.782051 |    0.75     | 0.703125 |   0.725806 |  0.844005 | [[77 15]           |         |         |          |               |
|                     |            |             |          |            |           |  [19 45]]          |         |         |          |               |
+---------------------+------------+-------------+----------+------------+-----------+--------------------+---------+---------+----------+---------------+
| Decision Tree       |   0.801282 |    0.851064 | 0.625    |   0.720721 |  0.846977 | [[85  7]           |         |         |          |               |
|                     |            |             |          |            |           |  [24 40]]          |         |         |          |               |
+---------------------+------------+-------------+----------+------------+-----------+--------------------+---------+---------+----------+---------------+
| Random Forest       |   0.814103 |    0.888889 | 0.625    |   0.733945 |  0.851053 | [[87  5]           |         |         |          |               |
|                     |            |             |          |            |           |  [24 40]]          |         |         |          |               |
+---------------------+------------+-------------+----------+------------+-----------+--------------------+---------+---------+----------+---------------+
| Linear Regression   |            |             |          |            |           |                    | 22.6138 | 45.6463 | 0.352817 |      0.317597 |
+---------------------+------------+-------------+----------+------------+-----------+--------------------+---------+---------+----------+---------------+

You should deploy the Random Forest classifier because it delivers the most robust and stable overall performance across nearly all critical classification metrics, including the highest Accuracy (0.814103), Precision (0.888889), F1 Score (0.733945), and ROC-AUC (0.851053).

Superior Overall Predictive Power: It achieves the highest Accuracy (81.41%) and ROC-AUC (0.851), proving it is the most reliable model at distinguishing between the two classes.Exceptional Precision (Lowest False Positives): With a Precision of 0.888889, it heavily outperforms Logistic Regression (0.750). The confusion matrix confirms it only made 5 False Positive errors (predicting survival when they didn't), compared to Logistic Regression's 15. This makes Random Forest ideal if a False Positive carries a high cost or risk.Best Balanced Metric (F1 Score): Despite its lower recall, its combined harmonic balance (F1 Score: 0.733945) is still the highest among all three models.

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

