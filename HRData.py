import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
df_hr = pd.read_csv('/content/HRDataset_v14.csv')
display(df_hr.head())
print("Dataset Information:")
df_hr.info()
print("\nDescriptive Statistics:")
display(df_hr.describe())
print("\nMissing Values per Column:")
display(df_hr.isnull().sum())
for column in df_hr.columns:
    if df_hr[column].dtype == 'object' or df_hr[column].nunique() < 20:
        print(f"\nUnique values for '{column}' ({df_hr[column].nunique()} unique):\n{df_hr[column].value_counts()}")
      # Select only numerical columns for correlation
numerical_df = df_hr.select_dtypes(include=np.number)

plt.figure(figsize=(18, 15))
sns.heatmap(numerical_df.corr(), annot=True, cmap='coolwarm', fmt=".2f")
plt.title('Correlation Heatmap of Numerical Features')
plt.show()df_hr.hist(figsize=(20, 15), bins=15)
plt.suptitle('Histograms of Numerical Features', y=1.02)
plt.tight_layout(rect=[0, 0.03, 1, 0.98])
plt.show()
plt.figure(figsize=(20, 15))
for i, column in enumerate(numerical_df.columns):
    plt.subplot(5, 4, i + 1) # Adjust subplot grid as needed
    sns.boxplot(y=df_hr[column])
    plt.title(column)
plt.suptitle('Box Plots of Numerical Features', y=1.02)
plt.tight_layout(rect=[0, 0.03, 1, 0.98])
plt.show()
# Example: Salary vs. EngagementSurvey
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df_hr, x='EngagementSurvey', y='Salary', hue='PerfScoreID', palette='viridis')
plt.title('Salary vs. Engagement Survey by Performance Score')
plt.xlabel('Engagement Survey Score')
plt.ylabel('Salary')
plt.show()

# Example: Salary vs. SpecialProjectsCount
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df_hr, x='SpecialProjectsCount', y='Salary', hue='Department', palette='tab10')
plt.title('Salary vs. Special Projects Count by Department')
plt.xlabel('Special Projects Count')
plt.ylabel('Salary')
plt.show()
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import seaborn as sns

# Prepare data for PCA
# Drop identifier columns and columns with too many unique values that are not suitable for direct PCA or that have missing values that would be better imputed (but for simplicity here, we drop).
# We will focus on numerical features that could represent a 'scale' or continuous measure.

pca_features = [
    'Salary', 'EngagementSurvey', 'EmpSatisfaction', 'SpecialProjectsCount',
    'Absences', 'DaysLateLast30', 'MarriedID', 'MaritalStatusID', 'GenderID',
    'EmpStatusID', 'DeptID', 'PerfScoreID', 'FromDiversityJobFairID', 'Termd'
]

df_pca = df_hr[pca_features].copy()

# Handle missing values: for ManagerID, we'll drop rows for PCA for simplicity
# Since ManagerID is not in pca_features, this step is for general awareness if we were to include it.
# For the selected pca_features, let's check if there are any nulls to drop.
# df_pca.isnull().sum() shows no nulls for these selected features.

# Standardize the data before applying PCA
scaler = StandardScaler()
scaled_data = scaler.fit_transform(df_pca)

pca = PCA(n_components=None) # Keep all components to evaluate explained variance
pca.fit(scaled_data)

# Plot the explained variance ratio
plt.figure(figsize=(10, 6))
plt.plot(np.cumsum(pca.explained_variance_ratio_))
plt.xlabel('Number of Components')
plt.ylabel('Cumulative Explained Variance')
plt.title('Explained Variance by Principal Components')
plt.grid(True)
plt.show()

# Show individual explained variance
print("Explained variance ratio of each principal component:")
print(pca.explained_variance_ratio_)

# Transform the data to the first few principal components (e.g., 2 for visualization)
pca_2_components = PCA(n_components=2)
principal_components = pca_2_components.fit_transform(scaled_data)
df_principal_components = pd.DataFrame(data=principal_components, columns=['principal component 1', 'principal component 2'])

# Optionally, visualize the first two principal components
plt.figure(figsize=(10, 8))
sns.scatterplot(
    x=df_principal_components['principal component 1'],
    y=df_principal_components['principal component 2'],
    hue=df_hr['Department'], # Example: color by a categorical variable
    palette='viridis'
)
plt.title('2 Principal Components of HR Data')
plt.xlabel('Principal Component 1')
plt.ylabel('Principal Component 2')
plt.grid(True)
plt.show()
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

# Define target and features
X = df_hr.drop('Salary', axis=1)
y = df_hr['Salary']

# Identify numerical and categorical features for the model
numerical_features = [
    'EngagementSurvey', 'EmpSatisfaction', 'SpecialProjectsCount',
    'Absences', 'DaysLateLast30', 'PerfScoreID', 'DeptID'
]
categorical_features = [
    'Position', 'Department', 'RecruitmentSource', 'PerformanceScore',
    'MaritalDesc', 'Sex'
]

# Create a preprocessor to handle numerical scaling and one-hot encoding for categorical features
preprocessor = ColumnTransformer(
    transformers=[
        ('num', 'passthrough', numerical_features),
        ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
    ],
    remainder='drop' # Drop columns not specified
)

# Create the pipeline: preprocessor + Linear Regression model
linear_model = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('regressor', LinearRegression())
])

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model
linear_model.fit(X_train, y_train)

# Make predictions on the test set
y_pred_linear = linear_model.predict(X_test)

# Evaluate the model
mse_linear = mean_squared_error(y_test, y_pred_linear)
r2_linear = r2_score(y_test, y_pred_linear)

print(f"Linear Regression Model Performance:")
print(f"Mean Squared Error (MSE): {mse_linear:.2f}")
print(f"R-squared (R2): {r2_linear:.2f}")

# Optionally, visualize predictions vs actual values
plt.figure(figsize=(10, 6))
sns.scatterplot(x=y_test, y=y_pred_linear)
plt.xlabel('Actual Salary')
plt.ylabel('Predicted Salary')
plt.title('Linear Regression: Actual vs. Predicted Salary')
plt.plot([y.min(), y.max()], [y.min(), y.max()], 'r--') # Plotting the ideal line
plt.grid(True)
plt.show()
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

# Define target and features for Logistic Regression (predicting 'Termd')
# For simplicity, we'll use a similar set of features as Linear Regression and some additional relevant ones.
# We need to make sure the target variable 'Termd' is not in the features.
X_lr = df_hr.drop(['Termd', 'Employee_Name', 'ManagerName', 'Position', 'Department', 'RecruitmentSource', 'PerformanceScore', 'MaritalDesc', 'Sex', 'DOB', 'DateofHire', 'DateofTermination', 'TermReason', 'EmploymentStatus', 'State', 'Zip'], axis=1)
y_lr = df_hr['Termd']

# Identify numerical and categorical features for the model
# Exclude 'EmpID', 'PositionID' if they are just identifiers and not meaningful for prediction
numerical_features_lr = [
    'EmpID', 'MarriedID', 'MaritalStatusID', 'GenderID', 'EmpStatusID',
    'DeptID', 'PerfScoreID', 'FromDiversityJobFairID', 'Salary', 'PositionID',
    'EngagementSurvey', 'EmpSatisfaction', 'SpecialProjectsCount', 'DaysLateLast30',
    'Absences'
]
categorical_features_lr = [] # We already dropped string categorical columns if they have high cardinality.

# Create a preprocessor for numerical scaling
# For simplicity, if no specific categorical features are identified, we use passthrough for numerical features.
# If there are categorical features that were not dropped, they need to be handled.
# Let's adjust based on the dropped columns above.

# Re-evaluating features to ensure only numerical or low-cardinality categorical are passed to preprocessor
# and that 'ManagerID' nulls are handled if included.

X_lr_temp = df_hr.drop(['Termd', 'Employee_Name', 'DateofTermination', 'LastPerformanceReview_Date', 'DOB', 'DateofHire'], axis=1).copy()

# Impute missing 'ManagerID' for Logistic Regression if it's included
if 'ManagerID' in X_lr_temp.columns:
    X_lr_temp['ManagerID'] = X_lr_temp['ManagerID'].fillna(X_lr_temp['ManagerID'].median())

# Separate feature types for preprocessing
numerical_features_lr = X_lr_temp.select_dtypes(include=np.number).columns.tolist()
categorical_features_lr = X_lr_temp.select_dtypes(include='object').columns.tolist()

preprocessor_lr = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), numerical_features_lr),
        ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features_lr)
    ],
    remainder='drop' # Drop any other columns not specified
)

# Create the pipeline: preprocessor + Logistic Regression model
logistic_model = Pipeline(steps=[
    ('preprocessor', preprocessor_lr),
    ('classifier', LogisticRegression(random_state=42, solver='liblinear')) # 'liblinear' handles L1/L2 penalties and small datasets well
])

# Split data into training and testing sets
X_train_lr, X_test_lr, y_train_lr, y_test_lr = train_test_split(X_lr_temp, y_lr, test_size=0.2, random_state=42, stratify=y_lr) # stratify for imbalanced classes

# Train the model
logistic_model.fit(X_train_lr, y_train_lr)

# Make predictions on the test set
y_pred_logistic = logistic_model.predict(X_test_lr)

# Evaluate the model
accuracy_lr = accuracy_score(y_test_lr, y_pred_logistic)
precision_lr = precision_score(y_test_lr, y_pred_logistic)
recall_lr = recall_score(y_test_lr, y_pred_logistic)
f1_lr = f1_score(y_test_lr, y_pred_logistic)
conf_matrix_lr = confusion_matrix(y_test_lr, y_pred_logistic)

print(f"Logistic Regression Model Performance:")
print(f"Accuracy: {accuracy_lr:.2f}")
print(f"Precision: {precision_lr:.2f}")
print(f"Recall: {recall_lr:.2f}")
print(f"F1-Score: {f1_lr:.2f}")
print(f"Confusion Matrix:\n{conf_matrix_lr}")

# Visualize Confusion Matrix
plt.figure(figsize=(8, 6))
sns.heatmap(conf_matrix_lr, annot=True, fmt='d', cmap='Blues',
            xticklabels=['Active', 'Terminated'], yticklabels=['Active', 'Terminated'])
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.title('Logistic Regression Confusion Matrix')
plt.show()
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report

# We will use the same preprocessor and split data (X_train_lr, y_train_lr, X_test_lr, y_test_lr)
# that was prepared for Logistic Regression.

# Create the pipeline: preprocessor + Decision Tree Classifier model
decision_tree_model = Pipeline(steps=[
    ('preprocessor', preprocessor_lr),
    ('classifier', DecisionTreeClassifier(random_state=42))
])

# Train the model
decision_tree_model.fit(X_train_lr, y_train_lr)

# Make predictions on the test set
y_pred_dt = decision_tree_model.predict(X_test_lr)

# Evaluate the model
accuracy_dt = accuracy_score(y_test_lr, y_pred_dt)
precision_dt = precision_score(y_test_lr, y_pred_dt)
recall_dt = recall_score(y_test_lr, y_pred_dt)
f1_dt = f1_score(y_test_lr, y_pred_dt)
conf_matrix_dt = confusion_matrix(y_test_lr, y_pred_dt)

print(f"Decision Tree Classifier Model Performance:")
print(f"Accuracy: {accuracy_dt:.2f}")
print(f"Precision: {precision_dt:.2f}")
print(f"Recall: {recall_dt:.2f}")
print(f"F1-Score: {f1_dt:.2f}")
print(f"Confusion Matrix:\n{conf_matrix_dt}")
print("\nClassification Report:\n", classification_report(y_test_lr, y_pred_dt))

# Visualize Confusion Matrix
plt.figure(figsize=(8, 6))
sns.heatmap(conf_matrix_dt, annot=True, fmt='d', cmap='Blues',
            xticklabels=['Active', 'Terminated'], yticklabels=['Active', 'Terminated'])
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.title('Decision Tree Confusion Matrix')
plt.show()
from sklearn.ensemble import RandomForestClassifier

# We will use the same preprocessor and split data (X_train_lr, y_train_lr, X_test_lr, y_test_lr)
# that was prepared for Logistic Regression.

# Create the pipeline: preprocessor + Random Forest Classifier model
random_forest_model = Pipeline(steps=[
    ('preprocessor', preprocessor_lr),
    ('classifier', RandomForestClassifier(random_state=42))
])

# Train the model
random_forest_model.fit(X_train_lr, y_train_lr)

# Make predictions on the test set
y_pred_rf = random_forest_model.predict(X_test_lr)

# Evaluate the model
accuracy_rf = accuracy_score(y_test_lr, y_pred_rf)
precision_rf = precision_score(y_test_lr, y_pred_rf)
recall_rf = recall_score(y_test_lr, y_pred_rf)
f1_rf = f1_score(y_test_lr, y_pred_rf)
conf_matrix_rf = confusion_matrix(y_test_lr, y_pred_rf)

print(f"Random Forest Classifier Model Performance:")
print(f"Accuracy: {accuracy_rf:.2f}")
print(f"Precision: {precision_rf:.2f}")
print(f"Recall: {recall_rf:.2f}")
print(f"F1-Score: {f1_rf:.2f}")
print(f"Confusion Matrix:\n{conf_matrix_rf}")
print("\nClassification Report:\n", classification_report(y_test_lr, y_pred_rf))

# Visualize Confusion Matrix
plt.figure(figsize=(8, 6))
sns.heatmap(conf_matrix_rf, annot=True, fmt='d', cmap='Blues',
            xticklabels=['Active', 'Terminated'], yticklabels=['Active', 'Terminated'])
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.title('Random Forest Confusion Matrix')
plt.show()
