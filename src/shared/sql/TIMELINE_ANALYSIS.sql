WITH milestone_timelines AS (
    SELECT 
        n.nda_id,
        n.governing_law,
        CAST(n.effective_date AS DATE) AS effective_date,
        m.name AS milestone_name,
        m.date AS milestone_date,
        DATEDIFF('day', CAST(n.effective_date AS DATE), m.date) AS days_from_effective
    FROM 
        ndas n
    JOIN 
        milestones m ON n.nda_id = m.nda_id
)
SELECT 
    mt.nda_id,
    substring(mt.governing_law, 1, 30) || '...' AS governing_law_abbrev,
    mt.milestone_name,
    mt.effective_date,
    mt.milestone_date,
    mt.days_from_effective,
    CASE 
        WHEN mt.days_from_effective < 365 THEN 'Less than 1 year'
        WHEN mt.days_from_effective BETWEEN 365 AND 730 THEN '1-2 years'
        WHEN mt.days_from_effective BETWEEN 731 AND 1825 THEN '2-5 years'
        ELSE 'More than 5 years'
    END AS time_category
FROM 
    milestone_timelines mt
ORDER BY 
    mt.nda_id, mt.days_from_effective;