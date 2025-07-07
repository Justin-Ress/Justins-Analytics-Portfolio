# Justin's Portfolio

## [Project 1: Explaining Improvement at the Elite Level of Swimming](https://public.tableau.com/app/profile/justin.ress/viz/100FREENCAAAnalysis/StartBreakoutDistanceTime)
## [Improvement in Swimming - Slides](https://docs.google.com/presentation/d/1oBngOtQkMqE9NKYmaXMpbXpXo549e3IrUyCKEplcpD8/edit?usp=sharing)

This is the first data project I completed, where I used data-driven insights to understand what it takes to improve in swimming at an elite level.

* I collected my own data for this project using a Python script I wrote that measures stroke rates across a race
* I ran the script for each 100 freestyle race in the A finals at the NCAA Championship from 2015-2024
* Upon the completion of the data collection, I wrote and ran different Python scripts to help aggregate and ogranize the data
* The resulting csv files were used to create compelling visuals with Tableau
* I found that swimmers were:
*   * An Average of 1.83 seconds faster in 2024 than 2015 
    * Taking Less Cycles (strokes) year over year. 20% less in 2024 than 2015
    * Maintaining similar stroke rates <1% change
    * Pushing Underwater kicks farther ~10 yards farther on average
    * Covering more ground per stroke ~5% more distance per cycle covered
* I used the visuals for a live presentation to club swimmers

## [Project 2: NCAA March Madness Predictive Models]

The second project I have completed involved learning about machine learning in order to create a predictive model for the NCAA Basketball Mens and Womens Tournaments.

* The first model I created was very basic as I was just understanding machine learning for the first time.
* I compared season long points per game and points against per game data from historical tournament matchups and built a model that would predict matchups based on the relationship between the teams.
* As you would expect, there was a lot of randomness in this model as it did not account for very in depth statistics or any strength of schedule metrics.
* Brier score on a 80/20 train/test split was around .1900, indicating that this was slightly better than random guessing.
* After understanding how the creation and implementation of the model worked, I then added raw statistical differences in my training dataset as well as 5 Key Performances Indicators (KPIs):
* KPIs: Average Possessions per game, a metric calcualted as a function of Offensive rebounds, Field Goals Attempted, Turnovers, and Free Throws attempted; Offensive Rating, calculated as Points per Poessisions; Defensive Rating, calculated as Points against per Possession; and Strength of Schedule, calculated as an average of opponents OFfensive and Defensive Ratings.
* My 5th KPI was a seed differential, calculated by subtracting Team 1 seed from Team 15.  This model gave me the best tested brier score and accuracy, around .1400 for men and .105 for women, and accuracy around 76% for men, 80% for women.
* However, when I used this model to fill out a bracekt, I was disappointed by the lack of upset predictions.  I wanted a model to try and predict some "madness" and go for big upsets.
* My first step was to add features that determine how hot or cold a team is.  So I added some features that compare how a team is playing at the end of the season to the full season.  i.e. (Offensive Rating_Trend = OffRtg(last 10 games) / OffRtg(Full season).  This gave me trends around 1.0, teams above 1.0 in these stats were playing better than earlier in the season, and teams below played worse.
* I also included a coference tournament win percentage feature to see if a team is winning in high pressure situations.
* This second model was able to predict some upsets, mainly among teams who were absolutely on fire end of season, like the 2024 NC State Wolfpack, which when testing the model on the 2024 tourney saw them upsetting Texas Tech in round 1.  However, there were still very few upset predictions, I had to do more digging.
* So I first looked into what my model was using as the most stand-out features.  Naturally, Seed differntial was the leading factor.  BSince so many 1v16 seed matchups exist, for example, and because nearly all 1 seeds won, the model would rely too heavily on seed differential, meaning upsets were never predicted.
* With this in mind I dropped my Seed Differential column and ended up with far more variation in upest prediction.  I used this model as my main model and so far it has been my most accurate for both men and women.
* I then built some models with only offensive stats in mind, defensive stats in mind, and end of season trends.  It was a very fun project that taught me how to search for key performance indicators and build models from them.

## [Project 3: Excitebike 64 Rider Performance Analysis](https://public.tableau.com/app/profile/justin.ress/viz/ExciteBikeDashboardv9/RiderProfiles)

This project was a passion project built around the game Excitebike 64, where I analyzed every track in the Pro Circuit for every rider to determine who performs best statistically—and why. I especially enjoyed this project because it brought data into something that likely hasn’t been analyzed at this level before.

Data Collection & Processing:
Recorded full race data (lap times, crashes, bad landings, race notes, and overheats) across three full Pro Circuit runs for all 6 riders

Collected all data manually and categorized race notes into qualitative indicators like:
* Sloppy Turn
* Close Finish
* Sloppy Race
* Clean Race

Used Python and Google Sheets to clean, transform, and aggregate all data

Derived Metrics:

* Flow Score: Measures race smoothness by factoring in crash frequency and sloppiness
* Pace Score: Measured from the variation in lap times across a rider's entire performance
* Recovery Score: Measured from an aggregate of crashes, bad landings, and rider interferance
* Surge Score:  Measured from the amount of times a rider appears in the top 5 lap times
* Track Difficulty Ratings: Derived from the coefficient of variation in lap times across all riders (Flow, Technical, Punisher, and Nightmare)

Additional Performance Stats:

* Clean Run %
* Top 3 Finish Rate
* Average Placement

Tableau Dashboards:

Rider Profiles Dashboard:
* Filterable bar charts with rider stats, data-driven stats, track specialization stats, and character bios

Track Leaderboard Dashboard:
* Lap-level comparison of each rider’s best races on all tracks
* Filterable by course and rider

Race Trends Summary Dashboard:
* Track difficulty vs. Flow Score, crash rate, and consistency metrics

Key Questions Answered:

* Who is the best rider on each track type?
* Which riders are more consistent vs. high-risk/high-reward?
* Where does each character struggle and why?
* If you were entering a tournament, which rider should you choose based on your play style?

This project combined my love for gaming and data and proved that even subjective experiences, like racing video games, can yield compelling, objective insights.









