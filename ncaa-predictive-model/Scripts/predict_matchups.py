import pandas as pd
import xgboost as xgb
import joblib  # For loading .pkl models

# ✅ Load the trained XGBoost model
model = joblib.load("C:\\Python\\MarchMadness\\v4\\Womens_Model_TrendsOnly.pkl")

# ✅ Load the new matchup dataset (WITHOUT labels)
df = pd.read_csv("H:\\NCAA March Madness 2025\\csv\\2025_WPrediction_Dataset.csv")

# ✅ Convert TeamID1 & TeamID2 to integers to remove ".0"
df["TeamID1"] = df["TeamID1"].astype(int)
df["TeamID2"] = df["TeamID2"].astype(int)

#rename columns correctly:
df = df.rename(columns={"PPG_Trend_Diff": "PPG_Diff_Trend_Diff","Opp_Avg_OffRtg_Trend_Diff": "Opp_Avg_OffRtg_1_Diff","Opp_Avg_DefRtg_Trend_Diff": "Opp_Avg_DefRtg_1_Diff"})

# Drop columns depending on which model you are using
df = df.drop(columns=["Seed_Diff","OR_Diff","Ast_Diff","Turnover_Diff","Avg_Possessions_Diff",
                                "OffRtg_Diff","Opp_Avg_DefRtg_Diff","DR_Diff","Stl_Diff","Blk_Diff","PF_Diff",
                                "DefRtg_Diff","FG%_Diff","FT%_Diff","PPG_Diff_Diff","3P%_Diff","Opp_Avg_OffRtg_Diff","Opp_Avg_DefRtg_Diff","SoS_Diff"], errors="ignore")
# ✅ Extract feature columns (everything except 'Season', 'TeamID1', 'TeamID2')
features = df.drop(columns=["Season", "TeamID1", "TeamID2"], errors='ignore')

# 🚀 Get expected feature names from the trained model
model_features = model.get_booster().feature_names

# 🚀 Get feature names from the test dataset
test_features = features.columns.tolist()

# Ensure the model matches the testing dataset
print("\n✅ Model expects these features:")
print(model_features)

print("\n✅ Test dataset has these features:")
print(test_features)

# 🚀 Find any mismatched features
missing_in_test = [col for col in model_features if col not in test_features]
extra_in_test = [col for col in test_features if col not in model_features]

print("\n⚠️ Missing in test dataset (model expects but not found):")
print(missing_in_test)

print("\n⚠️ Extra in test dataset (exists in test but not in model):")
print(extra_in_test)

# 🚀 Force feature alignment by keeping only the ones present in both
aligned_features = [col for col in model_features if col in test_features]
features = features[aligned_features]  # Keep only aligned features

# ✅ Make probability predictions
probabilities = model.predict_proba(features)[:, 1]  # Probability that Team1 wins

# ✅ Create the output format (TeamID1 and TeamID2 are separate)
df["Win_Probability"] = probabilities  # Store probability

# ✅ Keep only the necessary columns
output_df = df[["TeamID1", "TeamID2", "Win_Probability"]]

# ✅ Save predictions to CSV
output_df.to_csv("H:\\NCAA March Madness 2025\\csv\\2025_Women_TrendsOnlyPredictions.csv", index=False)

print("🎯 Predictions saved successfully! 🚀")
