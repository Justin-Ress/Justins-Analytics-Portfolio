# Import necessary libraries
import pandas as pd
import numpy as np
import joblib
import xgboost as xgb
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import brier_score_loss
import matplotlib.pyplot as plt

# 1 Load the dataset
file_path = "H:\\NCAA March Madness 2025\\csv\\WomensFullTrainingDataset.csv"  # Update path if needed
df_train = pd.read_csv(file_path)

# 2 Drop the columns you want so we can build different models.
df_train = df_train.drop(columns=["Seed_Diff","OR_Diff","Ast_Diff","Turnover_Diff","Avg_Possessions_Diff",
                                "OffRtg_Diff","Opp_Avg_DefRtg_Diff","DR_Diff","Stl_Diff","Blk_Diff","PF_Diff",
                                "DefRtg_Diff","FG%_Diff","FT%_Diff","PPG_Diff_Diff","3P%_Diff","Opp_Avg_OffRtg_Diff","Opp_Avg_DefRtg_Diff","SoS_Diff"], errors="ignore")
# 3 Define feature columns (excluding identifiers and target variable)
feature_columns = [col for col in df_train.columns if col not in ["TeamID1", "TeamID2", "Win", "Season"]]

# Define X (features) and y (target)
X = df_train[feature_columns]
y = df_train["Win"]



# 4 Split data into training (80%) and testing (20%) sets
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# 5 Define a more optimized parameter grid
param_grid = {
    "n_estimators": [100, 200, 300],  
    "learning_rate": [0.02, 0.03, 0.05],  
    "max_depth": [4, 5, 6],  
    "min_child_weight": [3, 5],  # Increase min_child_weight to require larger splits
    "subsample": [0.8, 0.9],  # Reduce to prevent trees from memorizing data
    "colsample_bytree": [0.7, 0.8, 0.9],  # Reduce reliance on all features
    "gamma": [0.1, 0.3, 0.5]  # ✅ Ensure there's a comma before this line
}


# 6 Initialize the XGBoost model with correct eval metric
xgb_model = xgb.XGBClassifier(
    objective="binary:logistic",
    eval_metric="logloss",
    random_state=42,
    early_stopping_rounds=50
)

# 7 Perform Grid Search with 5-fold cross-validation
grid_search = GridSearchCV(
    xgb_model,
    param_grid,
    scoring="neg_brier_score",
    cv=5,
    verbose=2,
    n_jobs=-1

)

# 8 Fit the grid search model to the training data with feature weights
grid_search.fit(X_train, y_train, eval_set=[(X_test, y_test)], verbose=False)

# Get the best model from the grid search
best_xgb_model = grid_search.best_estimator_

# Print the best hyperparameters found by Grid Search
best_params = grid_search.best_params_
print(f"Best Hyperparameters: {best_params}")

# 9 Extract feature importance
xgb_importances = best_xgb_model.feature_importances_
feat_importance_df = pd.DataFrame({"Feature": feature_columns, "Importance": xgb_importances})
feat_importance_df = feat_importance_df.sort_values(by="Importance", ascending=True)

# Plot the feature importance
plt.figure(figsize=(10, 6))
plt.barh(feat_importance_df["Feature"], feat_importance_df["Importance"], color="royalblue")
plt.xlabel("Feature Importance")
plt.ylabel("Feature Name")
plt.title("XGBoost Feature Importance")
plt.show()

# 10 Save the tuned model
model_path = "c:\\python\\Marchmadness\\v4\\Womens_Model_TrendsOnly.pkl"
joblib.dump(best_xgb_model, model_path)
print(f"Tuned model saved to {model_path}")
