# Processed Data

Cleaned and merged datasets used for model training.


### `MensFullTrainingDataset.csv` and `WomensFullTrainingDataset.csv`

These are the final datasets used to train the XGBoost models. Each row represents one historical NCAA tournament matchup, including:

- Team and seed info (`TeamID1`, `TeamID2`, `Seed_Diff`)
- Statistical differences (`PPG_Diff`, `OffRtg_Diff`, `FG%_Diff`, etc.)
- Trend differences (last 25-day performance changes)
- Conference tournament win % differences
- Binary outcome `Win` (1 if Team1 won)

