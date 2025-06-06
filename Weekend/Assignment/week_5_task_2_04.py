# -*- coding: utf-8 -*-
"""Week 5 task 2-04.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1tJIZBcEgcH14f9LREVtsnG1hlSX-i23W

4️⃣ Data Visualization
"""

import pandas as pd
from sklearn.preprocessing import MinMaxScaler, StandardScaler, LabelEncoder

def transform_data(df):
    # Ensure correct data types
    df['Annual_Income'] = df['Annual_Income'].astype(float)
    df['Spending_Score'] = df['Spending_Score'].astype(float)
    df['Purchase_Frequency'] = df['Purchase_Frequency'].astype(float)

    # Normalize Annual_Income and Spending_Score using Min-Max Scaling
    min_max_scaler = MinMaxScaler()
    df[['Annual_Income', 'Spending_Score']] = min_max_scaler.fit_transform(df[['Annual_Income', 'Spending_Score']])

    # Standardize Purchase_Frequency using Z-score Normalization
    standard_scaler = StandardScaler()
    df[['Purchase_Frequency']] = standard_scaler.fit_transform(df[['Purchase_Frequency']])

    # Convert Gender into numerical values using One-Hot Encoding
    df = pd.get_dummies(df, columns=['Gender'], drop_first=True)

    # Label encode the Preferred_Category column
    label_encoder = LabelEncoder()
    df['Preferred_Category'] = label_encoder.fit_transform(df['Preferred_Category'])

    return df

def feature_engineering(df):
    # Create Customer Loyalty Score
    def loyalty_score(row):
        if row['Spending_Score'] > 0.7 and row['Purchase_Frequency'] > 0.7:
            return 'High'
        elif row['Spending_Score'] > 0.4 and row['Purchase_Frequency'] > 0.4:
            return 'Medium'
        else:
            return 'Low'
    df['Customer_Loyalty_Score'] = df.apply(loyalty_score, axis=1)

    # Binning Annual Income
    income_bins = [0, 50000, 100000, float('inf')]
    income_labels = ['Low', 'Medium', 'High']
    df['Income_Level'] = pd.cut(df['Annual_Income'] * 100000, bins=income_bins, labels=income_labels)

    # Create Engagement Metric
    def engagement_status(row):
        if row['Last_Transaction_Days'] < 30 and row['Purchase_Frequency'] > 0.5:
            return 'Active'
        elif row['Last_Transaction_Days'] < 90:
            return 'Dormant'
        else:
            return 'Churned'
    df['Engagement_Status'] = df.apply(engagement_status, axis=1)

    return df

# Example usage
data = {
    'Annual_Income': [50000, 60000, 75000, 48000],
    'Spending_Score': [0.4, 0.7, 0.9, 0.2],
    'Purchase_Frequency': [0.5, 0.8, 1.2, 0.3],
    'Gender': ['Male', 'Female', 'Female', 'Male'],
    'Preferred_Category': ['Electronics', 'Clothing', 'Groceries', 'Clothing'],
    'Last_Transaction_Days': [10, 50, 120, 5]
}
df = pd.DataFrame(data)

df = transform_data(df)
df = feature_engineering(df)
print(df)