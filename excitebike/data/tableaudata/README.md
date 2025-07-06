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

### 🏁 Race Data with New Metrics

This file builds on the original raw race data by including new performance metrics and cleaned values for each run.

Each row represents a **single race run** and includes:

- **Original Race Info:**
  - Rider name
  - Run number
  - Cup and Course
  - Lap times and total time
  - Number of crashes, bad landings, and rider interferences
  - Overheat indicator
  - Final placement and race notes

- **Newly Calculated Metrics:**
  - **Flow Score:** Quantifies how smooth and uninterrupted a race was, based on notes and event flags
  - **Consistency (later called pace):** Measures lap time consistency (standard deviation within the race)
  - **Sloppiness Score (later inversed to Recovery Score):** Aggregated score from crashes, bad landings, and interference
  - **Clean Run Indicator:** Boolean flag for whether the run had *zero* negative events

This file supports race-by-race analysis and powers elements of the visual dashboards such as top 5 lap charts, flow ratings, and difficulty-based comparisons.


