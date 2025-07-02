# Trained Models

This folder contains trained XGBoost models saved as `.pkl` files using `joblib`. Each model was trained on a different subset of features to test different prediction strategies.

### Model Types

- **Trends Only**  
  Trained exclusively on how a team was playing at the end of the season.  
  Features are calculated as the ratio of last 30-day performance to full-season averages.  
  For example, a team averaging 100 PPG all season but only 50 PPG in the last 30 days would have a trend value of 0.5 for `PPG`.  
  These values are then compared to their opponent's trends to predict outcomes.

- **Only Defense**  
  Uses only defensive statistics such as defensive rebounds per game, points allowed, steals, and blocks.  
  Focuses on a team's ability to limit the opponent rather than score themselves.

- **Only Offense**  
  The inverse of the defensive model.  
  Trained only on offensive metrics like PPG, FG%, assists, and offensive rebounds.  
  Designed to test how far pure scoring ability can take a team in the tournament.

- **LoadedUp (No Seeds)**  
  Includes all statistical difference features from the training dataset **except seed information**.  
  Designed to encourage more upset predictions and reduce model bias toward high seeds.

- **LoadedUp**  
  Trained on the full feature set including seed differential, offensive and defensive KPIs, strength of schedule, and trend data.  
  This model is the most complete but tends to predict fewer upsets.

> These models are used in scripts such as `predict_matchups.py`, `evaluate_xgboost.py`, and `select_high_confidence_predictions.py`.
