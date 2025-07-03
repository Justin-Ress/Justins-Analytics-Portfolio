WITH ConfTourneyGames AS (
    -- Step 1: Select all conference tournament games
    SELECT 
        Season,
        ConfAbbrev,
        WTeamID AS TeamID,
        1 AS Win,
        0 AS Loss
    FROM `learning-435919.MarchMadness.WConfGames`
    
    UNION ALL
    
    SELECT 
        Season,
        ConfAbbrev,
        LTeamID AS TeamID,
        0 AS Win,
        1 AS Loss
    FROM `learning-435919.MarchMadness.WConfGames`
),

ConfTourneyWinPct AS (
    -- Step 2: Compute win percentage per team
    SELECT 
        Season,
        TeamID,
        ConfAbbrev,
        SUM(Win) AS Total_Wins,
        COUNT(*) AS Total_Games,
        SAFE_DIVIDE(SUM(Win), COUNT(*)) AS Conf_Tourney_WinPct  -- Avoid division by zero
    FROM ConfTourneyGames
    GROUP BY Season, TeamID, ConfAbbrev
)

-- Step 3: View results (or JOIN with main dataset later)
SELECT * 
FROM ConfTourneyWinPct
ORDER BY Season DESC, Conf_Tourney_WinPct DESC;
