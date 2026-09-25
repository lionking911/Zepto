# Titanic EDA Report

This document summarizes the exploratory data analysis (EDA) performed in `Analytics/eda.py` for the Titanic dataset.

## 1. Project Goal

The script is designed to:

- load the Titanic dataset from Seaborn if a local CSV is not available
- inspect structure, null values, and consistency issues
- clean and transform the dataset for analysis
- identify outliers and skewness
- visualize distributions and survival patterns
- generate a correlation-based summary of key numeric features

## 2. Data Source and Loading

The script checks whether `titanic.csv` already exists in the working directory:

- If the file is missing, it downloads the dataset using `sns.load_dataset("titanic")`
- It then saves the raw data as `titanic.csv`
- Otherwise, it reads the existing CSV and continues processing

This ensures the analysis is reproducible and avoids re-downloading the dataset each time.

## 3. Initial Data Inspection

The script runs a general profile of the dataset, including:

- `titanic.info()` to confirm column types and null counts
- `titanic.describe()` for central tendency and spread
- `titanic.shape` to print the row/column count

It also checks unique values in key categorical columns such as:

- `sex`
- `embarked`
- `class`
- `who`
- `deck`
- `embark_town`
- `alive`

This step helps identify inconsistencies, missing categories, and possible duplicate information.

## 4. Data Cleaning Strategy

### Missing values

The script calculates:

- total missing values per column
- missing value percentage per column

Important observations:

- `deck` has a very high missing percentage (around 77%) and is removed
- `embarked` has a very small number of missing values and rows are dropped
- `age` has missing values and is imputed with the mean

### Redundant or duplicate fields

The code checks whether some categorical columns encode the same information as others:

- `alive` vs `survived`
- `embark_town` vs `embarked`
- `class` vs `pclass`

If the values match, redundant columns are dropped to avoid duplicate signal in the model.

### Duplicates

The script removes duplicate rows using:

- `titanic.drop_duplicates(inplace=True)`

### Feature engineering

Two new columns are created:

- `alive_label` is mapped as `yes -> 1`, `no -> 0`
- `class_label` is mapped as `First -> 1`, `Second -> 2`, `Third -> 3`

These are used to validate redundancy and to simplify downstream analysis.

## 5. Outlier Analysis

Outliers are detected using the IQR method for numeric features:

- `fare`
- `age`

The script calculates:

- Q1 and Q3
- IQR
- upper and lower bounds
- number of records beyond the threshold

### Observed result

- `fare` had many outliers
- `age` also had a smaller set of outliers

These checks help decide whether to keep or transform extreme values.

## 6. Distribution and Skewness Analysis

The script computes summary statistics for both `fare` and `age`:

- mean
- median
- mode
- skewness

### Interpretation

- `age` appears approximately normal in distribution
- `fare` is right-skewed, with long tail behavior and a higher mean than median

This indicates that a small number of passengers paid unusually high fares, while most paid much less.

## 7. Visual Analysis

The script generates a multi-panel `matplotlib` + `seaborn` chart layout with the following plots:

1. Age histogram with KDE and mean/median/mode reference lines
2. Age box plot for outlier detection
3. Fare histogram with KDE and summary lines
4. Fare box plot
5. Correlation heatmap of restricted numeric columns
6. Age distribution by survival outcome
7. Fare distribution by survival outcome
8. Passenger count by gender and survival status
9. Passenger count by ticket class and survival status
10. Passenger count by embarkation port and survival status

## 8. Key EDA Findings

### Survival by gender

The analysis shows that women had a much higher survival rate than men.

This is a major signal in the Titanic dataset and is a common finding in historical survival analysis.

### Survival by class

Passengers in first and second class tended to survive more often than passengers in third class.

This suggests that socioeconomic status and cabin location influenced survival chances.

### Survival by fare

Lower fare passengers are more represented among non-survivors, while higher fare passengers have a stronger survival pattern.

This reinforces the relationship between wealth and access to safer deck positions and evacuation priority.

### Embarkation port

Southampton has the largest passenger count, and it also shows a high number of non-survivors.

## 9. Correlation Summary

The script restricts the dataset to the following numeric columns:

- `survived`
- `pclass`
- `age`
- `sibsp`
- `parch`
- `fare`

It calculates the Pearson correlation matrix and prints the strongest off-diagonal relationships.

This helps identify the strongest numeric associations without relying on all variables in the dataset.

## 10. Data Scaling Example

The script finishes by standardizing selected columns (`age` and `fare`) using `StandardScaler`:

- `scaler = StandardScaler()`
- `scaled_matrix = scaler.fit_transform(titanic[["age", "fare"]])`

It then prints the mean and standard deviation of the scaled data to confirm the transformed features have approximately zero mean and unit variance.

## 11. Outputs

The script creates or uses the following files:

- `titanic.csv` — downloaded/raw dataset
- `cleaned_titanic.csv` — cleaned dataset after preprocessing
- visual plots via `matplotlib` and `seaborn`

## 12. Dependencies

This project uses:

- `pandas`
- `seaborn`
- `matplotlib`
- `scikit-learn`

## 13. How to Run

From the repository root, run:

```bash
python Analytics/eda.py
```

This will:

- load or fetch the dataset
- perform cleaning and exploratory analysis
- print key summaries to the console
- display the generated charts

## 14. Summary

The EDA shows that the Titanic dataset contains several clear signals related to survival:

- women survived more than men
- higher-class passengers had better survival odds
- lower fares were associated with higher fatalities
- age and fare distributions reveal important data-shape characteristics

This analysis provides a strong statistical foundation for any subsequent predictive modeling or feature preparation work.
