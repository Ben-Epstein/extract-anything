WITH party_summary AS (
    SELECT 
        n.nda_id,
        n.title,
        n.agreement_type,
        n.governing_law,
        COUNT(DISTINCT p.party_name) AS party_count,
        STRING_AGG(DISTINCT p.party_role, ', ') AS party_roles,
        STRING_AGG(DISTINCT p.party_type, ', ') AS party_types,
        COUNT(DISTINCT CASE WHEN p.party_role = 'DISCLOSING_PARTY' THEN p.party_name END) AS disclosing_parties,
        COUNT(DISTINCT CASE WHEN p.party_role = 'RECEIVING_PARTY' THEN p.party_name END) AS receiving_parties
    FROM 
        ndas n
    JOIN 
        parties p ON n.nda_id = p.nda_id
    GROUP BY 
        n.nda_id, n.title, n.agreement_type, n.governing_law
)
SELECT 
    ps.agreement_type,
    ps.party_roles,
    ps.party_count,
    COUNT(DISTINCT ps.nda_id) AS agreement_count,
    ROUND(AVG(CASE WHEN r.severity = 'HIGH' THEN 1.0 WHEN r.severity = 'MEDIUM' THEN 0.5 ELSE 0 END), 2) AS avg_risk_score,
    COUNT(DISTINCT CASE WHEN r.severity = 'HIGH' THEN r.nda_id END) AS agreements_with_high_risk,
    ps.governing_law
FROM 
    party_summary ps
LEFT JOIN 
    risks r ON ps.nda_id = r.nda_id
GROUP BY 
    ps.agreement_type, ps.party_roles, ps.party_count, ps.governing_law
ORDER BY 
    avg_risk_score DESC, agreement_count DESC;