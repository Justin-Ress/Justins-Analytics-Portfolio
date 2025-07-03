WITH TeamStats AS (
    -- Your existing query calculating team season averages
    SELECT 
        TeamID,
        Season,
        AVG(Off_R) AS `OR`,
        AVG(Def_R) AS DR,
        AVG(Assist) AS Ast,
        AVG(Turnover) AS Turnover,
        AVG(Steal) AS Stl,
        AVG(Block) AS Blk,
        AVG(Personal_Foul) AS PF,
        AVG(possessions) AS Avg_Possessions,
        AVG(offensive_rating) AS OffRtg,
        AVG(defensive_rating) AS DefRtg,
        AVG(FG_Perc) AS `FG%`,
        AVG(FT_Perc) AS `FT%`,
        AVG(points_scored - points_allowed) AS PPG_Diff,
        AVG(Three_Perc) AS `3P%`
    FROM (
        -- When the team wins
        SELECT 
            WTeamID AS TeamID,
            Season, 
            WScore AS points_scored, 
            LScore AS points_allowed,
            (WFGA - WOR + WTO + (0.44 * WFTA)) AS possessions,
            (WScore / NULLIF((WFGA - WOR + WTO + (0.44 * WFTA)), 0)) * 100 AS offensive_rating,  
            (LScore / NULLIF((WFGA - WOR + WTO + (0.44 * WFTA)), 0)) * 100 AS defensive_rating,  
            WOR AS Off_R,
            WDR AS Def_R,
            WAst AS Assist,
            WStl AS Steal,
            WBlk AS Block,
            WPF AS Personal_Foul,
            (WFGM / NULLIF(WFGA, 0)) AS FG_Perc,
            (WFTM / NULLIF(WFTA, 0)) AS FT_Perc,
            (WFGM3 / NULLIF(WFGA3, 0)) AS Three_Perc,
            WTO AS Turnover
        FROM `learning-435919.MarchMadness.MRegularSeasonDetailedResults`
        UNION ALL
        -- When the team loses
        SELECT 
            LTeamID AS TeamID,
            Season,
            LScore AS points_scored, 
            WScore AS points_allowed,
            (LFGA - LOR + LTO + (0.44 * LFTA)) AS possessions,
            (LScore / NULLIF((LFGA - LOR + LTO + (0.44 * LFTA)), 0)) * 100 AS offensive_rating,  
            (WScore / NULLIF((LFGA - LOR + LTO + (0.44 * LFTA)), 0)) * 100 AS defensive_rating,
            LOR AS Off_R,
            LDR AS Def_R,
            LAst AS Assist,
            LStl AS Steal,
            LBlk AS Block,
            LPF AS Personal_Foul,
            (LFGM / NULLIF(LFGA, 0)) AS FG_Perc,
            (LFTM / NULLIF(LFTA, 0)) AS FT_Perc,
            (LFGM3 / NULLIF(LFGA3, 0)) AS Three_Perc,
            LTO AS Turnover 
        FROM `learning-435919.MarchMadness.MRegularSeasonDetailedResults`
    )
    GROUP BY TeamID, Season
),
OpponentStats AS (
    -- Get the average Offensive and Defensive Ratings of Opponents
    SELECT 
        t1.TeamID,
        t1.Season,
        AVG(t2.OffRtg) AS Opp_Avg_OffRtg,
        AVG(t2.DefRtg) AS Opp_Avg_DefRtg
    FROM `learning-435919.MarchMadness.MRegularSeasonDetailedResults` AS games
    JOIN TeamStats t1 ON games.WTeamID = t1.TeamID OR games.LTeamID = t1.TeamID
    JOIN TeamStats t2 ON (games.WTeamID = t2.TeamID OR games.LTeamID = t2.TeamID) AND t1.Season = t2.Season
    WHERE t1.TeamID != t2.TeamID  -- Exclude self-matches
    GROUP BY t1.TeamID, t1.Season
)

SELECT 
    ts.*,
    os.Opp_Avg_OffRtg,
    os.Opp_Avg_DefRtg,
    -- Strength of Schedule Calculation (Weighted)
    (0.5 * os.Opp_Avg_OffRtg + 0.5 * os.Opp_Avg_DefRtg) AS SoS
FROM TeamStats ts
JOIN OpponentStats os ON ts.TeamID = os.TeamID AND ts.Season = os.Season;
