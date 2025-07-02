import pandas as pd

# Load datasets
season_data = pd.read_csv("H:\\NCAA March Madness 2025\\csv\\WomensDataset_toCreateTraining.csv")  # Contains full-season stats + trends + seeds
matchups = pd.read_csv("H:\\NCAA March Madness 2025\\csv\\WomensTourneyMatchups.csv")  # Contains tournament matchups

# Merge season data with matchups (for both teams)
df = matchups.merge(season_data, left_on=['Season', 'WTeamID'], right_on=['Season', 'TeamID'], suffixes=("_Team1", ""))
df = df.merge(season_data, left_on=['Season', 'LTeamID'], right_on=['Season', 'TeamID'], suffixes=("_Team1", "_Team2"))

# Rename columns correctly
df = df.rename(columns={"WTeamID": "TeamID1", "LTeamID": "TeamID2"})

# Drop redundant TeamID columns
df = df.drop(columns=['TeamID_Team1', 'TeamID_Team2'])



# Load a sample dataset to get column names
df_sample = season_data.copy()  # Copy to avoid modifying the original DataFrame

# List of columns to exclude (i.e., ones we don't want to subtract)
exclude_columns = {"Season", "TeamID", "Seed_Team1", "Seed_Team2", "TeamID1", "TeamID2", "Win"}

# Dynamically select numeric stat columns to subtract
stat_columns = [col for col in df_sample.columns if col not in exclude_columns]

print("Selected stat columns for subtraction:", stat_columns)


# Compute stat differences (Team1 - Team2)
for stat in stat_columns:
    df[f"{stat}_Diff"] = df[f"{stat}_Team1"] - df[f"{stat}_Team2"]


# Assign win/loss outcome (1 = Team1 won, 0 = Team1 lost)
df["Win"] = 1

# Create reversed matchups (Team1 <-> Team2, outcome flipped)
df_reversed = df.copy()

# Reverse matchups (Team1 <-> Team2)
df_reversed = df_reversed.rename(columns={"TeamID1": "Temp", "TeamID2": "TeamID1"})
df_reversed = df_reversed.rename(columns={"Temp": "TeamID2"})  # Swap complete


df_reversed[[f"{stat}_Diff" for stat in stat_columns]] = -df_reversed[[f"{stat}_Diff" for stat in stat_columns]]
df_reversed["Win"] = 0  # Flip win/loss

# Combine original and reversed matchups
final_df = pd.concat([df, df_reversed], ignore_index=True)

# Keep only relevant columns: Season, TeamIDs, stat differences, Seed_Diff, Win
columns_to_keep = ["Season", "TeamID1", "TeamID2", "Win"] + [f"{stat}_Diff" for stat in stat_columns]

# Drop non-difference columns
final_df = final_df[columns_to_keep]

# Save the cleaned dataset
final_df.to_csv("WomensFullTrainingDataset.csv", index=False)

print("Final training dataset created successfully!")



