# Import necessary libraries
import pandas as pd
import numpy as np
import joblib
import xgboost as xgb
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import brier_score_loss

# 1️⃣ Load the dataset
file_path = "H:\\NCAA March Madness 2025\\csv\\MensTrainingDataset.csv"  # Update path if needed
df = pd.read_csv(file_path)

# 2️⃣ Drop categorical conference columns for training
df_train = df.drop(columns=["Conf_Team1", "Conf_Team2"], errors="ignore")

# Define feature columns (excluding identifiers and target variable)
feature_columns = [col for col in df_train.columns if col not in ["TeamID1", "TeamID2", "Win", "Season"]]

# Define X (features) and y (target)
X = df_train[feature_columns]
y = df_train["Win"]

# Handle potential missing values (if any)
X = X.fillna(0)

# 3️⃣ Split data into training (80%) and testing (20%) sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# 4️⃣ Define an optimized parameter grid for tuning
param_grid = {
    "n_estimators": [100, 200, 300],  
    "learning_rate": [0.03, 0.05, 0.1],  
    "max_depth": [5, 6, 7],  
    "min_child_weight": [1, 3],  
    "subsample": [0.8, 1.0],  
    "colsample_bytree": [0.8, 1.0],  
    "gamma": [0, 0.1, 0.2]  # Prevent overfitting
}

# 5️⃣ Initialize the XGBoost model with proper evaluation metrics
xgb_model = xgb.XGBClassifier(
    objective="binary:logistic",
    eval_metric="logloss",
    random_state=42,
)

# 6️⃣ Perform Grid Search with 5-fold cross-validation
grid_search = GridSearchCV(
    xgb_model,
    param_grid,
    scoring="neg_brier_score",  # Optimize for Brier Score
    cv=5,  
    verbose=2,  
    n_jobs=-1  
)

# 7️⃣ Fit the grid search model to the training data
grid_search.fit(X_train, y_train)

# Get the best model from the grid search
best_xgb_model = grid_search.best_estimator_

# Extract feature importance from the best XGBoost model
xgb_importances = best_xgb_model.feature_importances_

# Create a DataFrame for visualization
feat_importance_df = pd.DataFrame({"Feature": feature_columns, "Importance": xgb_importances})
feat_importance_df = feat_importance_df.sort_values(by="Importance", ascending=True)

# Plot the feature importance
plt.figure(figsize=(10, 6))
plt.barh(feat_importance_df["Feature"], feat_importance_df["Importance"], color="royalblue")
plt.xlabel("Feature Importance")
plt.ylabel("Feature Name")
plt.title("XGBoost Feature Importance")
plt.show()

# Print the best hyperparameters found by Grid Search
best_params = grid_search.best_params_
print(f"Best Hyperparameters: {best_params}")

# Evaluate the model on the test set
y_pred_prob = best_xgb_model.predict_proba(X_test)[:, 1]
brier_score = brier_score_loss(y_test, y_pred_prob)
print(f"Brier Score on Test Set: {brier_score:.5f}")

# 8️⃣ Save the tuned model
model_path = "C:\\Python\\Marchmadness\\v4\\xgb_marchmadness_Mens_SymmetricalModel.pkl"  # Update path if needed
joblib.dump(best_xgb_model, model_path)
print(f"Tuned model saved to {model_path}")
