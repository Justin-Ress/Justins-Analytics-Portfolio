-- Builds final training dataset by joining historical tournament matchups
-- with full-season and trend stats, then computing stat differences

SELECT 
    m.Season,
    m.TeamID1,
    m.TeamID2,
    m.Seed_Team1,
    m.Seed_Team2,
    (CAST(m.Seed_Team2 AS INT) - CAST(m.Seed_Team1 AS INT)) AS Seed_Diff,

    -- PPG Difference (unique per team)
    t1.`PPG_Diff%` AS `PPG_Diff%_Team1`,
    t2.`PPG_Diff%` AS `PPG_Diff%_Team2`,

    -- Raw stat differences (Team1 - Team2)
    (t1.OR - t2.OR) AS OR_Diff,
    (t1.DR - t2.DR) AS DR_Diff,
    (t1.TO - t2.TO) AS TO_Diff,
    (t1.Stl - t2.Stl) AS Stl_Diff,
    (t1.Blk - t2.Blk) AS Blk_Diff,
    (t1.PF - t2.PF) AS PF_Diff,
    (t1.Avg_Possessions - t2.Avg_Possessions) AS Avg_Possessions_Diff,
    (t1.OffRtg - t2.OffRtg) AS OffRtg_Diff,
    (t1.DefRtg - t2.DefRtg) AS DefRtg_Diff,
    (t1.Opp_OffRtg - t2.Opp_OffRtg) AS Opp_OffRtg_Diff,
    (t1.Opp_DefRtg - t2.Opp_DefRtg) AS Opp_DefRtg_Diff,
    (t1.SoS - t2.SoS) AS SoS_Diff,
    (t1.`FG%` - t2.`FG%`) AS `FG%_Diff`,
    (t1.`FT%` - t2.`FT%`) AS `FT%_Diff`,
    (t1.`3P%` - t2.`3P%`) AS `3P%_Diff`,

    -- Trend differences (Team1 - Team2)
    (t1.OR_Trend - t2.OR_Trend) AS OR_Trend_Diff,
    (t1.DR_Trend - t2.DR_Trend) AS DR_Trend_Diff,
    (t1.Ast_Trend - t2.Ast_Trend) AS Ast_Trend_Diff,
    (t1.TO_Trend - t2.TO_Trend) AS TO_Trend_Diff,
    (t1.Stl_Trend - t2.Stl_Trend) AS Stl_Trend_Diff,
    (t1.Blk_Trend - t2.Blk_Trend) AS Blk_Trend_Diff,
    (t1.PF_Trend - t2.PF_Trend) AS PF_Trend_Diff,
    (t1.Poss_Trend - t2.Poss_Trend) AS Poss_Trend_Diff,
    (t1.OffRtg_Trend - t2.OffRtg_Trend) AS OffRtg_Trend_Diff,
    (t1.Opp_OffRtg_Trend - t2.Opp_OffRtg_Trend) AS Opp_OffRtg_Trend_Diff,
    (t1.Opp_DefRtg_Trend - t2.Opp_DefRtg_Trend) AS Opp_DefRtg_Trend_Diff,
    (t1.PPG_Diff - t2.PPG_Diff) AS PPG_Trend_Diff,
    (t1.FG_Trend - t2.FG_Trend) AS FG_Trend_Diff,
    (t1.FT_Trend - t2.FT_Trend) AS FT_Trend_Diff,
    (t1.Three_Trend - t2.Three_Trend) AS `3P_Trend_Diff`,

    -- Conference performance (Team1 - Team2)
    (t1.Conf_Tourney_WinPct - t2.Conf_Tourney_WinPct) AS Conf_Tourney_WinPct_Diff,

    -- Win label (1 = Team1 wins, 0 = Team2 wins)
    CASE WHEN m.WTeamID = m.TeamID1 THEN 1 ELSE 0 END AS Win

FROM `learning-435919.MarchMadness.MensTourneyMatchups` m
JOIN `learning-435919.MarchMadness.Combined_FinalSeason` t1 
    ON m.TeamID1 = t1.TeamID AND m.Season = t1.Season
JOIN `learning-435919.MarchMadness.Combined_FinalSeason` t2 
    ON m.TeamID2 = t2.TeamID AND m.Season = t2.Season;
