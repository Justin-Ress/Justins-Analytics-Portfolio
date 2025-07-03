# SQL Queries

This folder contains all BigQuery SQL scripts used to extract, clean, and prepare NCAA basketball data for training and testing predictive models. These scripts powered the creation of training datasets, trend-based features, and tournament matchup inputs.

---

## 📄 Query Descriptions

### `conference_tourney_records.sql`  
Calculates each team’s win percentage in their conference tournament for each season.  
- Combines win/loss data from Conference Games csv
- Aggregates total wins and games played per team
- Outputs: `Season`, `TeamID`, `ConfAbbrev`, `Wins`, `Games`, `Conf_Tourney_WinPct`  
> Used to evaluate teams' performance in high-pressure postseason games.

---

### `fullseasondata_trends.sql`  
Creates trend-based features by comparing each team’s last 25 days of play to their full-season performance.  
- Joins last-25-day and full-season stats
- Computes stat ratios (e.g., `OffRtg_Trend = OffRtg_Last25 / OffRtg_Season`)
- Values ~1.0 indicate steady performance; >1.0 = improving; <1.0 = declining  
> Used to capture momentum heading into the NCAA tournament.

---

### `season_base_averages.sql`  
Produces core season-level team stats used in all models.  
Includes:
- Points per game, field goal %, assists, rebounds, turnovers, etc.
- Offensive Rating, Defensive Rating
- Opponent average stats to compute Strength of Schedule (SoS)  
> This forms the statistical foundation of predictive features.

---

### `season_derived_kpis.sql`  
Generates advanced or creative KPIs based on play-by-play event ratios.  
Metrics include:
- `Sloppy_Play_Index`, `Hack_A_Shaq_Rate`, `Boom_or_Bust`
- `Stl_Ast_Ratio`, `Hustle_Index`, `Assist_Dependency`, and more  

---

### `training_dataset.sql`

Builds the final **training dataset** used for model development by joining historical tournament matchups with full-season stats and performance trends.

**Key features:**
- Merges `TeamID1` and `TeamID2` from historical matchups with their corresponding stats
- Computes differences between teams for:
  - Raw stats (e.g., `OR_Diff`, `DefRtg_Diff`)
  - Performance trends from last 25 days (e.g., `OR_Trend_Diff`, `FG_Trend_Diff`)
  - Conference tournament win % (`Conf_Tourney_WinPct_Diff`)
- Adds a binary label column `Win` (1 if Team1 won, 0 otherwise)
- Used to create the primary training CSV used by all XGBoost models

**Source Tables Used:**
- `MensTourneyMatchups`: All historical NCAA tournament matchups (with winner/loser)
- `Combined_FinalSeason`: Preprocessed season + trend metrics for each team-year

> This query is the backbone of the predictive model — it gives the model both long-term averages and short-term momentum indicators to learn from.

