This contains cleaned data used for Tableau Dashboards:

### 👤 Clean Character Data

This file contains summarized rider-level data across all races, used to power the character radar charts and stat comparisons.

Each row represents one rider and includes:

- **Identifying Columns:**
  - Rider name
  - Rider alias or label used in visualizations

- **In-Game Stats:**
  - Cornering
  - Jumping
  - Landing
  - Turbo

- **Derived Performance Metrics:**
  - **Flow Score Rating:** Measures how smoothly a rider maintained momentum, based on Python-scripted translations of race notes (e.g. avoiding crashes and rider interference).
  - **Recovery Rating:** Inverse of a sloppiness metric derived from crashes, bad landings, and interference events.
  - **Average Time:** Mean total race time across all runs.
  - **Pace Rating:** Based on the standard deviation of lap times within races—lower values indicate more consistent pacing.
  - **Surge Rating:** Counts how often a rider appeared in the top 5 fastest laps across all races, then scaled to a 1–10 score.
  - **Adaptability Score:** Scrapped metric; previously tested for rider performance across track types.
  - **Personal Preference:** My own subjective impression of the rider.

- **Track-Type Performance:**
  - Average race times and points for each difficulty group: *Flow*, *Technical*, *Punisher*, and *Nightmare*
  - Ratings (1–10) for performance on each track type, derived from both average time and points

- **Race Summary Stats:**
  - Average Placement
  - Win %
  - Top 3 Finish %
  - Average Points (overall and by track type)

- **Character Bio:**
  - Narrative summary of how each rider performed, based on trends observed throughout the project

This cleaned dataset serves as the basis for the rider profile dashboard and enables direct comparison between character styles, strengths, and performance consistency.

