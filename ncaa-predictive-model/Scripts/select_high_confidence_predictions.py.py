import pandas as pd

# Manually specify your 5 model files
file_paths = [
    "H:\\NCAA March Madness 2025\\csv\\2025_WLoadedupPredictions_NoSeeds.csv",
    "H:\\NCAA March Madness 2025\\csv\\2025_WLoadedupPredictions.csv",
    "H:\\NCAA March Madness 2025\\csv\\2025_WLoadedupPredictions_OnlyOffense.csv",
    "H:\\NCAA March Madness 2025\\csv\\2025_WLoadedupPredictions_OnlyDefense.csv",
    "H:\\NCAA March Madness 2025\\csv\\2025_Women_TrendsOnlyPredictions.csv"
]

# Load them into a dictionary
model_dfs = {fp.replace('.csv', ''): pd.read_csv(fp) for fp in file_paths}
 
# Ensure all files have 'TeamID1', 'TeamID2', and 'Pred' columns
for name, df in model_dfs.items():
    if not {'TeamID1', 'TeamID2', 'Pred'}.issubset(df.columns):
        raise ValueError(f"{name} is missing required columns.")

# Identify the main model (Change to the actual filename without .csv)
MAIN_MODEL = "H:\\NCAA March Madness 2025\\csv\\2025_WLoadedupPredictions_NoSeeds".replace('.csv', '')
main_df = model_dfs[MAIN_MODEL].copy()

# Create final submission
final_preds = []

for _, row in main_df.iterrows():
    team1 = row['TeamID1']
    team2 = row['TeamID2']
    main_pred = row['Pred']
    main_winner = 1 if main_pred >= 0.50 else 2  # Team1 wins if Pred >= 0.50, else Team2

    best_conf = main_pred  # Default to main model's prediction
    
    for model_name, df in model_dfs.items():
        if model_name == MAIN_MODEL:
            continue  # Skip the main model, we already checked it

        # Get the model's prediction for this game
        model_pred = df.loc[(df['TeamID1'] == team1) & (df['TeamID2'] == team2), 'Pred'].values
        if len(model_pred) == 0:
            continue  # Skip if model doesn't have this game
        
        model_pred = model_pred[0]
        model_winner = 1 if model_pred >= 0.50 else 2

        # If the model agrees with the main model's winner, update confidence selection
        if model_winner == main_winner:
            if main_winner == 1:  # If Team 1 wins, pick the highest confidence
                if abs(model_pred - 0.50) > abs(best_conf - 0.50):
                    best_conf = model_pred
            else:  # If Team 2 wins, pick the lowest confidence
                if model_pred < best_conf:  
                    best_conf = model_pred
    
    final_preds.append({'TeamID1': team1, 'TeamID2': team2, 'Pred': best_conf})

# Convert to DataFrame and save final submission
final_df = pd.DataFrame(final_preds)
final_df.to_csv("final_submission.csv", index=False)

print("Final submission file 'final_submission.csv' generated successfully!")
