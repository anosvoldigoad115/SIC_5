# -*- coding: utf-8 -*-
"""SIC 5_Technical Assignment_2.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Q84thigS5bguYFQQthi9glv1GLFfjnHY

# **Part 1: Data Preparation**

**1. Import Libraries and Load Dataset**
"""

import pandas as pd

# Load dataset
file_path = 'ai4i2020.csv'
dataset = pd.read_csv(file_path)

# Display initial information about the dataset
print(dataset.info())

# Display initial information about the dataset
print(dataset.head())

"""**2. Data Preprocessing**"""

from sklearn.preprocessing import StandardScaler, LabelEncoder

# Check for missing values
print(dataset.isnull().sum())

# Encode categorical variables
label_encoder = LabelEncoder()
dataset['Product ID'] = label_encoder.fit_transform(dataset['Product ID'])
dataset['Type'] = label_encoder.fit_transform(dataset['Type'])

# Features and target variable
features = dataset.drop(columns=['UDI', 'Machine failure', 'TWF', 'HDF', 'PWF', 'OSF', 'RNF'])
target = dataset['TWF']

"""# **Part 2: Splitting Data and Normalization**

**3. Data Splitting and Normalization**
"""

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# Split the dataset
X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)

# Normalize numerical features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

"""# **Part 3: Handling Imbalanced Data**

**4. Handling Imbalanced Data with SMOTE (Synthetic Minority Over-sampling Technique)**
"""

from imblearn.over_sampling import SMOTE

# Apply SMOTE to balance the dataset
smote = SMOTE(random_state=42)
X_train_balanced, y_train_balanced = smote.fit_resample(X_train_scaled, y_train)

"""# **Part 4: Model Training and Evaluation**

**5. Training and Evaluating the Random Forest Model**
"""

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report

# Train the Random Forest model
rf_model_balanced = RandomForestClassifier(random_state=42)
rf_model_balanced.fit(X_train_balanced, y_train_balanced)

# Predict on the test set
y_pred_balanced = rf_model_balanced.predict(X_test_scaled)

# Evaluate the model
accuracy_balanced = accuracy_score(y_test, y_pred_balanced)
precision_balanced = precision_score(y_test, y_pred_balanced)
recall_balanced = recall_score(y_test, y_pred_balanced)
f1_balanced = f1_score(y_test, y_pred_balanced)
classification_rep_balanced = classification_report(y_test, y_pred_balanced)

print(f'Accuracy: {accuracy_balanced}')
print(f'Precision: {precision_balanced}')
print(f'Recall: {recall_balanced}')
print(f'F1 Score: {f1_balanced}')
print('Classification Report:')
print(classification_rep_balanced)