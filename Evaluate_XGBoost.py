# Import necessary libraries
import pandas as pd
import joblib
import xgboost as xgb
from sklearn.metrics import brier_score_loss, accuracy_score, log_loss
from sklearn.model_selection import train_test_split

# 1 Load the dataset (same dataset used for training)
file_path = "H:\\NCAA March Madness 2025\\csv\\MensFullTrainingDataset.csv"  # Update path if needed
df_test = pd.read_csv(file_path)

# 2 Drop columns to evaluate different models.
df_test = df_test.drop(columns=["Seed_Diff","OR_Diff","Ast_Diff","Turnover_Diff","Avg_Possessions_Diff",
                                "OffRtg_Diff","Opp_Avg_DefRtg_Diff","DR_Diff","Stl_Diff","Blk_Diff","PF_Diff",
                                "DefRtg_Diff","FG%_Diff","FT%_Diff","PPG_Diff_Diff","3P%_Diff","Opp_Avg_OffRtg_Diff","Opp_Avg_DefRtg_Diff","SoS_Diff"], errors="ignore")

# Define feature columns (excluding identifiers and target variable)
feature_columns = [col for col in df_test.columns if col not in ["TeamID1", "TeamID2", "Win", "Season"]]

# Define X (features) and y (target)
X = df_test[feature_columns]
y = df_test["Win"]

# 3 Split data into training (80%) and testing (20%) sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 4 Load the tuned XGBoost model
model_path = "c:\\python\\Marchmadness\\v4\\Mens_Model_TrendsOnly.pkl"  # Update path if needed
xgb_model = joblib.load(model_path)

# 5 Make probability predictions on the test set
y_pred_proba = xgb_model.predict_proba(X_test)[:, 1]  # Probability that Team1 wins

# 6 Test Different Decision Thresholds
best_acc = 0
best_threshold = 0.5  # Default threshold
accuracy_results = {}

print("\n🔹 **Testing Different Decision Thresholds** 🔹")
for threshold in [.45,.48,.50,.53,.56]:
    y_pred = (y_pred_proba > threshold).astype(int)
    acc = accuracy_score(y_test, y_pred)
    accuracy_results[threshold] = acc
    
    # Store best threshold
    if acc > best_acc:
        best_acc = acc
        best_threshold = threshold

    print(f"Threshold {threshold:.2f} → Accuracy: {acc:.4f}")

# ✅ Apply Best Threshold for Final Prediction
y_pred_final = (y_pred_proba > best_threshold).astype(int)

# 7️⃣ Evaluate Model Performance with Best Threshold
final_accuracy = accuracy_score(y_test, y_pred_final)
final_brier = brier_score_loss(y_test, y_pred_proba)
final_log_loss = log_loss(y_test, y_pred_proba)

# Ensure you use the correct trained model variable (replace with yours)
train_accuracy = xgb_model.score(X_train, y_train)
test_accuracy = xgb_model.score(X_test, y_test)

print(f"Train Accuracy: {train_accuracy:.4f}")
print(f"Test Accuracy: {test_accuracy:.4f}")



print("\n🔹 **Final Model Performance Using Best Threshold** 🔹")
print(f"✅ Best Threshold: {best_threshold:.2f}")
print(f"✅ Accuracy: {final_accuracy:.4f}")
print(f"✅ Brier Score: {final_brier:.4f}")
print(f"✅ Log Loss: {final_log_loss:.4f}")




