WITH TeamStats AS (
    -- Combine stats for games when a team won and when they lost
    SELECT 
        Season,
        WTeamID AS TeamID,
        COUNT(*) AS Games_Played,
        SUM(WStl) AS Total_Stl,
        SUM(WFTA) as Total_FTA, 
        SUM(WTO) AS Total_TO,
        SUM(WBlk) as Total_Blk,
        SUM(WPF) as Total_PF,
        SUM(WAst) AS Total_Ast,
        SUM(WFGM) as Total_FGM,
        Sum(LPF) as Total_PF_Against,
        SUM(WFGA) AS Total_FGA,
        SUM(WFGM3) AS Total_3PM, 
        SUM(WFGA3) AS Total_3PA,
        SUM(WFGA - WOR + WTO + (0.44 * WFTA)) AS Total_Possessions  
    FROM `learning-435919.MarchMadness.MRegularSeasonDetailedResults`
    GROUP BY Season, WTeamID

    UNION ALL

    SELECT 
        Season,
        LTeamID AS TeamID,
        COUNT(*) AS Games_Played,
        SUM(LPF) as Total_PF,
        SUM(LFGM) as Total_FGM,
        Sum(WPF) as Total_PF_Against,
        SUM(LBlk) as Total_Blk,
        SUM(LFTA) as Total_FTA,
        SUM(LTO) AS Total_TO,
        SUM(LStl) AS Total_Stl, 
        SUM(LAst) AS Total_Ast,
        SUM(LFGA) AS Total_FGA,
        SUM(LFGM3) AS Total_3PM, 
        SUM(LFGA3) AS Total_3PA,
        SUM(LFGA - LOR + LTO + (0.44 * LFTA)) AS Total_Possessions
    FROM `learning-435919.MarchMadness.MRegularSeasonDetailedResults`
    GROUP BY Season, LTeamID
),

AggregatedStats AS (
    -- Sum up stats for teams across all their games
    SELECT
        Season,
        TeamID,
        -- New metrics:
        SAFE_DIVIDE(SUM(Total_TO), SUM(Total_Possessions)) 
        + SAFE_DIVIDE(SUM(Total_PF), SUM(Total_Possessions)) AS Sloppy_Play_Index,
        SAFE_DIVIDE(SUM(Total_FTA), SUM(Total_FGA)) AS Hack_A_Shaq_Rate,
        SAFE_DIVIDE(SUM(Total_Stl), SUM(Total_TO)) AS Live_Ball_TO_Rate,
        SAFE_DIVIDE(SUM(Total_3PA) + SUM(Total_FTA), SUM(Total_FGA)) AS Three_or_Key,
        SAFE_DIVIDE(SUM(Total_Ast), SUM(Total_FGM)) AS Assist_Dependency,
        SAFE_DIVIDE(SUM(Total_Stl) + SUM(Total_Blk), SUM(Total_Possessions)) AS Hustle_Index,
        SAFE_MULTIPLY(SAFE_DIVIDE(SUM(Total_3PM), SUM(Total_3PA)), SAFE_DIVIDE(SUM(Total_TO), SUM(Total_Possessions))) AS Boom_or_Bust,
        SAFE_DIVIDE(SUM(Total_Stl), SUM(Total_Ast)) AS Stl_Ast_Ratio, -- Steal-to-Assist Ratio
        SAFE_DIVIDE(SUM(Total_TO), SUM(Total_Possessions)) AS Turnover_Percentage,
        SAFE_DIVIDE(SUM(Total_FTA), SUM(Total_PF_Against)) AS Ref_Whistle_Index,
 
        SAFE_DIVIDE(SUM(Total_3PA), SUM(Total_FGA)) AS `3%ShootingrateOfTotalFg` -- % of shots that are 3-pointers
    FROM TeamStats
    GROUP BY Season, TeamID
)

-- ✅ Step 2: Merge into 2025MFinalData
SELECT * FROM AggregatedStats
