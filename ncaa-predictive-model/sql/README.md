# SQL Queries

This folder contains all BigQuery SQL scripts used to extract, clean, and prepare NCAA basketball data for training and testing predictive models. These scripts powered the creation of training datasets, trend-based features, and tournament matchup inputs.

---

## 📄 Query Descriptions

### `conference_tourney_records.sql`  
Calculates each team’s win percentage in their conference tournament for each season.  
- Combines win/loss data from `WConfGames`
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
> This forms the statistical foundation of your predictive features.

---

### `season_derived_kpis.sql`  
Generates advanced or creative KPIs based on play-by-play event ratios.  
Metrics include:
- `Sloppy_Play_Index`, `Hack_A_Shaq_Rate`, `Boom_or_Bust`
- `Stl_Ast_Ratio`, `Hustle_Index`, `Assist_Dependency`, and more  
> Can be optionally joined to `season_base_averages` using `Season` and `Team
