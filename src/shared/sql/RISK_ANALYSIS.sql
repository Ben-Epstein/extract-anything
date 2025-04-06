SELECT 
    n.agreement_type,
    COUNT(*) AS total_agreements,
    ROUND(AVG(n.confidentiality_period_length), 2) AS avg_confidentiality_period,
    COUNT(CASE WHEN r.severity = 'HIGH' THEN 1 END) AS high_risk_count,
    COUNT(DISTINCT r.nda_id) AS agreements_with_risks,
    ROUND(COUNT(CASE WHEN r.severity = 'HIGH' THEN 1 END) * 100.0 / COUNT(*), 2) AS high_risk_percentage
FROM 
    ndas n
LEFT JOIN 
    risks r ON n.nda_id = r.nda_id
GROUP BY 
    n.agreement_type
ORDER BY 
    high_risk_percentage DESC;