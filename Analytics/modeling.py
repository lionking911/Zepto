import pandas as pd
import numpy as np
from tabulate import tabulate
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split,GridSearchCV
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier,plot_tree
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LinearRegression
from imblearn.pipeline import Pipeline 
from imblearn.over_sampling import SMOTE
import joblib
from sklearn.metrics import (
    accuracy_score, 
    precision_score, 
    recall_score, 
    f1_score, 
    roc_auc_score, 
    confusion_matrix, 
    roc_curve, 
    ConfusionMatrixDisplay,
    classification_report,
    auc,
    mean_absolute_error,
    mean_squared_error,
    r2_score,
    precision_recall_fscore_support
)

comparision_list=[]
#  DATA LOADING & TRAIN-TEST SPLIT


df = pd.read_csv("cleaned_titanic.csv")

# Define Features and Target
X = df[['pclass', 'sex', 'age', 'sibsp', 'parch', 'fare', 'embarked']]
y = df['survived']

# Stratified Split to preserve class proportions (Survived vs Died ratio)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, 
    test_size=0.2, 
    stratify=y, 
    random_state=42
)

#  PIPELINE & COLUMNTRANSFORMER SETUP
 
num_features = ['age', 'fare', 'sibsp', 'parch']
cat_features = ['pclass', 'sex', 'embarked']

# Sub-pipeline for Numerical features
num_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='mean')),
    ('scaler', StandardScaler())
])

# Sub-pipeline for Categorical features
cat_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('onehot', OneHotEncoder(handle_unknown='ignore', drop='first'))
])

# Combine preprocessing branches
preprocessor = ColumnTransformer(
    transformers=[
        ('num', num_transformer, num_features),
        ('cat', cat_transformer, cat_features)
    ])

# Create the final main pipeline containing Preprocessing + Estimator
clf_pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('classifier', LogisticRegression(max_iter=1000))
])

 
#  MODEL TRAINING & PREDICTION
 
clf_pipeline.fit(X_train, y_train)

# Generate hard classifications and probability estimates
y_pred = clf_pipeline.predict(X_test)
y_pred_proba = clf_pipeline.predict_proba(X_test)[:, 1]

 
#  METRIC COMPUTATION & EVALUATION
 
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)
roc_auc = roc_auc_score(y_test, y_pred_proba)



print("============ Logestic Performances Metrics ============")
print(f"Accuracy:  {accuracy:.4f}")
print(f"Precision: {precision:.4f}")
print(f"Recall:    {recall:.4f}")
print(f"F1 Score:  {f1:.4f}")
print(f"ROC AUC:   {roc_auc:.4f}\n")

print("Classification Report:\n", classification_report(y_test, y_pred))

 
#  VISUALIZATION (Confusion Matrix & ROC)
 
fig, ax = plt.subplots(1, 2, figsize=(14, 5))

# Plot Confusion Matrix
cm = confusion_matrix(y_test, y_pred)
dict=["Logistic Regression",accuracy,precision,recall,f1,roc_auc,cm]
comparision_list.append(dict)
print(f" Confusion_Matrix:\n",cm)
cm_display = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=['Died (0)', 'Survived (1)'])
cm_display.plot(ax=ax[0], cmap='Blues', values_format='d')
ax[0].set_title('Confusion Matrix')

# Plot ROC Curve
fpr, tpr, thresholds = roc_curve(y_test, y_pred_proba)
ax[1].plot(fpr, tpr, color='darkorange', lw=2, label=f'ROC Curve (AUC = {roc_auc:.2f})')
ax[1].plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--') # Baseline / Random guess line
ax[1].set_xlim([0.0, 1.0])
ax[1].set_ylim([0.0, 1.05])
ax[1].set_xlabel('False Positive Rate (1 - Specificity)')
ax[1].set_ylabel('True Positive Rate (Sensitivity / Recall)')
ax[1].set_title('Receiver Operating Characteristic (ROC) Curve')
ax[1].legend(loc="lower right")
ax[1].grid(True, linestyle='--', alpha=0.6)

plt.tight_layout()
plt.show()
print("============ DecisionTreeClassifier ============")
#  Create final modeling pipeline with Decision Tree Classifier
clf_pipeline= Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        ("classifier", DecisionTreeClassifier(max_depth=5, random_state=42))
    ]
)

#  Train-Test Split with 'stratify' to preserve target class distribution
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)

#  Fit the model Pipeline
clf_pipeline.fit(X_train, y_train)
#  Extract dynamic feature names after preprocessing transformation
# The preprocessor moves the encoded 'sex' column first, followed by remainder columns

raw_feature_names = clf_pipeline.named_steps[
    "preprocessor"
].get_feature_names_out()
clean_feature_names = [name.split("__")[-1] for name in raw_feature_names]
class_names = ["Perished", "Survived"]





#  Generate Predictions
y_pred = clf_pipeline.predict(X_test)
y_pred_proba = clf_pipeline.predict_proba(X_test)[:, 1]  # Probabilities needed for ROC-AUC

  
# Model Evaluation and Plotting Metrics
accuracy=accuracy_score(y_test, y_pred)
precision=precision_score(y_test, y_pred)
recall=recall_score(y_test, y_pred)
f1=f1_score(y_test, y_pred)
roc_auc=roc_auc_score(y_test, y_pred_proba)
# Print out textual metrics
print("--- Classification Performance Metrics ---")
print(f"Accuracy  : {accuracy:.4f}")
print(f"Precision : {precision:.4f}")
print(f"Recall    : {recall:.4f}")
print(f"F1 Score  : {f1:.4f}")
print(f"ROC AUC   : {roc_auc:.4f}\n")



print("Classification Report:\n", classification_report(y_test, y_pred))

# Initialize subplots for Confusion Matrix & ROC Curve side-by-side
fig, axes = plt.subplots(1, 2, figsize=(14, 5))
sns.set_theme(style="whitegrid")

#  Confusion Matrix
cm = confusion_matrix(y_test, y_pred)
dict=["Decision Tree",accuracy,precision,recall,f1,roc_auc,cm]
comparision_list.append(dict)
print(f" Confusion_Matrix:\n",cm)
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=["Not Survived", "Survived"])
disp.plot(ax=axes[0], cmap="Blues", values_format="d")
axes[0].set_title("Confusion Matrix")


#  ROC Curve & AUC
fpr, tpr, thresholds = roc_curve(y_test, y_pred_proba)
#auc_score = roc_auc_score(y_test, y_pred_proba)

axes[1].plot(fpr, tpr, color="darkorange", lw=2, label=f"ROC curve (AUC = {roc_auc:.2f})")
axes[1].plot([0, 1], [0, 1], color="navy", lw=2, linestyle="--")  # Baseline diagonal
axes[1].set_xlim([0.0, 1.0])
axes[1].set_ylim([0.0, 1.05])
axes[1].set_xlabel("False Positive Rate (FPR)")
axes[1].set_ylabel("True Positive Rate (TPR)")
axes[1].set_title("Receiver Operating Characteristic (ROC) Curve")
axes[1].legend(loc="lower right")



plt.tight_layout()
plt.show()

#  Render the tree using plot_tree
plt.figure(figsize=(36, 12), dpi=300)
plot_tree(
    clf_pipeline[-1],
    feature_names=clean_feature_names,
    class_names=class_names,
    filled=True,
    rounded=True,
    fontsize=9,
    precision=2
)

plt.title(
    "Titanic Survival Prediction - Decision Tree Pipeline",
    fontsize=14,
    pad=20,
)
plt.show()

print("============ RandomForestClassifier ============")
#  Create Final Pipeline with Random Forest Classifier
model_pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('classifier', RandomForestClassifier(n_estimators=100, random_state=42, max_depth=6)) 
])

#  Train the model
model_pipeline.fit(X_train, y_train)
complete_pipeline_X_train=X_train
complete_pipeline_y_train=y_train
#  Generate Predictions
y_pred = model_pipeline.predict(X_test)
y_pred_proba = model_pipeline.predict_proba(X_test)[:, 1] # Target probabilities for ROC-AUC

#  Compute and Print Classification Metrics
print("--- RANDOM FOREST PERFORMANCE METRICS ---")
accuracy=accuracy_score(y_test, y_pred)
precision=precision_score(y_test, y_pred)
recall=recall_score(y_test, y_pred)
f1=f1_score(y_test, y_pred)
roc_auc=roc_auc_score(y_test, y_pred_proba)
# Print out textual metrics
print("--- Classification Performance Metrics ---")
print(f"Accuracy  : {accuracy:.4f}")
print(f"Precision : {precision:.4f}")
print(f"Recall    : {recall:.4f}")
print(f"F1 Score  : {f1:.4f}")
print(f"ROC AUC   : {roc_auc:.4f}\n")
print("Classification Report:\n", classification_report(y_test, y_pred))
#  Visualization: Confusion Matrix & ROC Curve side-by-side
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

sns.set_theme(style="whitegrid")
# Plot A: Confusion Matrix
cm = confusion_matrix(y_test, y_pred)
dict=["Random Forest",accuracy,precision,recall,f1,roc_auc,cm]
comparision_list.append(dict)
print(f" Confusion_Matrix:\n",cm)
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=['Died (0)', 'Survived (1)'])
disp.plot(ax=axes[0], cmap='Blues', values_format='d')
axes[0].set_title('Confusion Matrix')

# Plot B: ROC Curve & AUC Score
fpr, tpr, thresholds = roc_curve(y_test, y_pred_proba)
#roc_auc = auc(fpr, tpr)
print(f" AUC   : {roc_auc:.4f}\n")
axes[1].plot(fpr, tpr, color='darkorange', lw=2, label=f'ROC curve (AUC = {roc_auc:.2f})')
axes[1].plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
axes[1].set_xlim([0.0, 1.0])
axes[1].set_ylim([0.0, 1.05])
axes[1].set_xlabel('False Positive Rate')
axes[1].set_ylabel('True Positive Rate')
axes[1].set_title('Receiver Operating Characteristic (ROC) Curve')
axes[1].legend(loc="lower right")

plt.tight_layout()
plt.show()


print("============ Evaluate all three models  ============")
headers = ["Model", "Accuracy","Precision","Recall" ,"F1 Score", "ROC-AUC","Confusion-Matrix"]
print(tabulate(comparision_list, headers=headers, tablefmt="grid"))
#print(f"        Model               Accuracy                Precision                   Recall                  F1-Score            Roc AUC             Confusion Matrix")
#for i in comparision_list:
   #print(f"{i["model"]}     { i["accuracy"]:.4f}        {i["precision"]:.4f}        {i["recall"]:.4f}       {i["f1"]:.4f}       {i["roc_auc"]:.4f}        {i["cm"]}")


print("============ Handling imbalance ============")
# --- Step : Report Class Balance ---
print("=== Class Balance Report ===")
balance = y.value_counts()
percentage = y.value_counts(normalize=True) * 100
for cls in balance.index:
    label = "Survived" if cls == 1 else "Not-Survived"
    print(f"{label} (Class {cls}): {balance[cls]} samples ({percentage[cls]:.2f}%)")
print("=" * 28 + "\n")

# --- Step : Stratified Train-Test Split ---
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)

# --- Step : Define ColumnTransformer for Preprocessing ---
numeric_features = ['age', 'fare']
numeric_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler())
])

categorical_features = ['sex', 'pclass', 'embarked']
categorical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('encoder', OneHotEncoder(drop='first', handle_unknown='ignore'))
])

preprocessor = ColumnTransformer(transformers=[
    ('num', numeric_transformer, numeric_features),
    ('cat', categorical_transformer, categorical_features)
])

# Dictionary to hold final evaluation metrics
results = {}

   
# Variant (a): Baseline / No Handling
   
pipeline_baseline = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('classifier', LogisticRegression(random_state=42))
])
pipeline_baseline.fit(X_train, y_train)
y_pred_base = pipeline_baseline.predict(X_test)
results['Baseline (No Handling)'] = precision_recall_fscore_support(y_test, y_pred_base, average='binary')

   
# Variant (b): class_weight='balanced'
   
pipeline_balanced = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('classifier', LogisticRegression(class_weight='balanced', random_state=42))
])
pipeline_balanced.fit(X_train, y_train)
y_pred_bal = pipeline_balanced.predict(X_test)
results['Class Weight Balanced'] = precision_recall_fscore_support(y_test, y_pred_bal, average='binary')

   
# Variant (c): SMOTE Oversampling (Applied only to Train Fold)
   
pipeline_smote = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('smote', SMOTE(random_state=42)), # Imblearn Pipeline applies this ONLY during training
    ('classifier', LogisticRegression(random_state=42))
])
pipeline_smote.fit(X_train, y_train)
y_pred_smote = pipeline_smote.predict(X_test)
results['SMOTE (Train Fold Only)'] = precision_recall_fscore_support(y_test, y_pred_smote, average='binary')

# --- Step : Compare Performance Metrics ---
df_compare = pd.DataFrame(results, index=['Precision', 'Recall', 'F1-Score', 'Support']).drop('Support')
print("=== Performance Comparison (Target: Survived Class) ===")
print(df_compare.round(3))

print("============ Hyperparameter tuning ============")


#  Construct the pipeline with oob_score=True
# Note: oob_score=True must be set at instantiation time
pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('classifier', RandomForestClassifier(oob_score=True, random_state=42))
])

# 5. Define the hyperparameter grid
# Prefix parameter names with the classifier step name followed by '__'
param_grid = {
    'classifier__n_estimators':[1000],
    'classifier__max_depth': [5, 10, None],
    'classifier__max_features': ['sqrt', 'log2']
}

#  Run GridSearchCV
grid_search = GridSearchCV(estimator=pipeline, param_grid=param_grid, cv=5, n_jobs=-1)
grid_search.fit(X, y)

#  Extract the best model and corresponding OOB score
best_pipeline = grid_search.best_estimator_
best_rf_model = best_pipeline.named_steps['classifier']
oob_score = best_rf_model.oob_score_

#  Report the results
print(f"Best Parameter Combination: {grid_search.best_params_}")
print(f"Corresponding Out-of-Bag (OOB) Score: {oob_score:.4f}")

print("============ Liner Regression ============")


# Define features and target
#features = 
target = 'fare'

# Drop rows where the target variable itself is missing (if any)
df = df.dropna(subset=[target])

X = df[['pclass', 'sex', 'age', 'sibsp', 'parch', 'embarked']]
y = df[target]


#  Stratified Train-Test Split (80% Train, 20% Test)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

#  Define Preprocessing Pipelines for Numerical and Categorical Features
numeric_features = ['age', 'sibsp', 'parch', 'pclass']
categorical_features = ['sex', 'embarked']

numeric_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler())
])

categorical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('onehot', OneHotEncoder(drop='first', handle_unknown='ignore'))
])

# Combine transformers using ColumnTransformer
preprocessor = ColumnTransformer(
    transformers=[
        ('num', numeric_transformer, numeric_features),
        ('cat', categorical_transformer, categorical_features)
    ]
)

#  Create the Master Pipeline (Preprocessing + Model)
model_pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('regressor', LinearRegression())
])

#  Train the Model Pipeline
model_pipeline.fit(X_train, y_train)

#  Make Predictions on Test Data
y_pred_test = model_pipeline.predict(X_test)

#  Calculate Performance Metrics
mae = mean_absolute_error(y_test, y_pred_test)
rmse = np.sqrt(mean_squared_error(y_test, y_pred_test))
r2 = r2_score(y_test, y_pred_test)

# Calculate Adjusted R²
n = len(y_test)
p = X_test.shape[1] + 2  # Approximate number of features after one-hot encoding
adjusted_r2 = 1 - (1 - r2) * (n - 1) / (n - p - 1)

# Print Metrics
print("--- Pipeline & Stratified Split Metrics (Test Set) ---")
print(f"Mean Absolute Error (MAE)  : {mae:.2f}")
print(f"Root Mean Squared Error (RMSE): {rmse:.2f}")
print(f"R² Score                   : {r2:.4f}")
print(f"Adjusted R² Score          : {adjusted_r2:.4f}\n")

#  Calculate Residuals
residuals_test = y_test - y_pred_test

#  Plot Residuals
plt.figure(figsize=(10, 6))
sns.scatterplot(x=y_pred_test, y=residuals_test, alpha=0.7, color='darkcyan', edgecolor='w')
plt.axhline(y=0, color='red', linestyle='--', linewidth=2)

plt.title('Residual Plot using scikit-learn Pipeline ', fontsize=14)
plt.xlabel('Predicted Fare', fontsize=12)
plt.ylabel('Residuals (Actual - Predicted)', fontsize=12)
plt.grid(True, linestyle=':', alpha=0.6)

plt.show()

#this plot demonstrates a classic, example of severe heteroscedasticity. as its in cone shape or funnel shape
print("============ model comparison table  ============")
comparision_list.append(['Linear Regression','','','','','','',mae,rmse,r2,adjusted_r2])
sub_headers = ["Model", "Accuracy","Precision","Recall" ,"F1 Score", "ROC-AUC","Confusion-Matrix","MAE","RMSE","R2","Adjusted R2"]

table_str = tabulate(comparision_list, headers=sub_headers, tablefmt="grid")
lines = table_str.split("\n")


top_border = lines[0]  
parts = top_border.split('+')[1:-1]
widths = [len(p) for p in parts]


w_model = widths[0]                               
w_class = sum(widths[1:6]) + 4                   
w_reg = sum(widths[6:10]) + 3                    


top_header_text = f"| {'Model Info'.center(w_model)} | {'Classification Metrics'.center(w_class)} | {'Regression Metrics'.center(w_reg)} |"
top_border_new = "+" + "-"*w_model + "+" + "-"*w_class + "+" + "-"*w_reg + "+"


final_table = "\n".join([top_border_new, top_header_text, lines[0], lines[1], lines[2]] + lines[3:])


print(final_table)
print("============ Final complete pipeline  ============")

# Create the full end-to-end Pipeline
full_pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('classifier', RandomForestClassifier(random_state=42))
])

# Fit the entire preprocessing framework and estimator at once
full_pipeline.fit(complete_pipeline_X_train, complete_pipeline_y_train)
print("✅ Full preprocessing and estimation pipeline fitted successfully.")

# Save the full pipeline object to disk
model_filename = 'full_prediction_pipeline.joblib'
joblib.dump(full_pipeline, model_filename)
print(f"💾 Saved complete artifact to disk as: '{model_filename}'\n")


print("--- Reloading & Validation on Raw Inputs ---")

# Reload the unified architecture from disk
loaded_pipeline = joblib.load(model_filename)
print("🔄 End-to-end pipeline loaded back from disk.")

# Build a brand new raw data chunk with severe challenges (missing entries, unseen category)
new_raw_input = pd.DataFrame({
    "pclass":[3,1],
    "sex":["male","female"],
    'age': [22,38],
    "sibsp":[1,1],
    'parch': [0,0],
    'fare': [8,72],  # 'Mumbai' was not in training; handled safely by 'ignore' flag
    'embarked':["S","C"]
})

# Predict directly on raw inputs without explicit manual preprocessing
predictions = loaded_pipeline.predict(new_raw_input)
probabilities = loaded_pipeline.predict_proba(new_raw_input)[:, 1]

# Display validation metrics
for idx, (pred, prob) in enumerate(zip(predictions, probabilities)):
    print(f"Sample {idx+1} Raw Input Predicted Output Class: {pred} (Positive Probability: {prob:.2f})")
