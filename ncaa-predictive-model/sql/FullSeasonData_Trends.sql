-- this query takes teh full season data that we gathered from previous queries and normalizes the last 25 day trends so that they are all around 1.0

SELECT 
    f.TeamID,
    f.Season,

    -- Keep all full-season stats
    f.OR,
    f.DR,
    f.Ast,
    f.Turnover,
    f.Stl,
    f.Blk,
    f.PF,
    f.Avg_Possessions,
    f.OffRtg,
    f.DefRtg,
    f.`FG%`,
    f.`FT%`,
    f.PPG_Diff,
    f.`3P%`,
    f.Opp_Avg_OffRtg,
    f.Opp_Avg_DefRtg,
    f.SoS,

    -- Compute trend values (Last 25 Days / Full Season)
    (l.OR_trend / NULLIF(f.OR, 0)) AS OR_Trend,
    (l.DR_trend / NULLIF(f.DR, 0)) AS DR_Trend,
    (l.Ast_trend / NULLIF(f.Ast, 0)) AS Ast_Trend,
    (l.Turnover_trend / NULLIF(f.Turnover, 0)) AS Turnover_Trend,
    (l.Stl_trend / NULLIF(f.Stl, 0)) AS Stl_Trend,
    (l.Blk_trend / NULLIF(f.Blk, 0)) AS Blk_Trend,
    (l.PF_trend / NULLIF(f.PF, 0)) AS PF_Trend,
    (l.Avg_Possessions_trend / NULLIF(f.Avg_Possessions, 0)) AS Avg_Possessions_Trend,
    (l.OffRtg_trend / NULLIF(f.OffRtg, 0)) AS OffRtg_Trend,
    (l.DefRtg_trend / NULLIF(f.DefRtg, 0)) AS DefRtg_Trend,
    (l.`FG%_trend` / NULLIF(f.`FG%`, 0)) AS `FG%_Trend`,
    (l.`FT%_trend` / NULLIF(f.`FT%`, 0)) AS `FT%_Trend`,
    (l.PPG_Diff_trend / NULLIF(f.PPG_Diff, 0)) AS PPG_Diff_Trend,
    (l.`3P%_trend` / NULLIF(f.`3P%`, 0)) AS `3P%_Trend`,
    (l.Opp_Avg_OffRtg / NullIF(f.Opp_Avg_OffRtg,0)) as Opp_Avg_OffRtg,
    (l.Opp_Avg_DefRtg / NullIF(f.Opp_Avg_DefRtg,0)) as Opp_Avg_DefRtg,
    (l.SoS / NullIF(f.SoS,0)) as SoS_Trend

FROM `learning-435919.MarchMadness.WomensFullSeasonAverages` f
JOIN `learning-435919.MarchMadness.WomensLast25DaysAverages` l 
ON f.TeamID = l.TeamID AND f.Season = l.Season;
