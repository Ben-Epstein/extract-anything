from pathlib import Path

import duckdb
import polars as pl

from shared.gcs import get_hmac_keys

SQLS = Path(__file__).parent / "sql"


def configure_duckdb_gcs_delta():
    con = duckdb.connect(db_path, read_only=False)
    con.execute("USE main;")
    secrets = con.query("FROM duckdb_secrets() where type='gcs'")
    views = con.query("FROM duckdb_views where view_name in ('ndas', 'parties', 'risks', 'milestones')")
    if len(secrets) == 1 and len(views) == 4:
        return con
    key, secret = get_hmac_keys()
    con.execute(f"""
    CREATE OR REPLACE PERSISTENT SECRET (
        TYPE gcs,
        KEY_ID '{key}',
        SECRET '{secret}'
    );
    """)
    con.execute("CREATE OR REPLACE VIEW ndas AS SELECT * FROM delta_scan('gs://northeastern-pdf-ndas/db/ndas');")
    con.execute("CREATE OR REPLACE VIEW parties AS SELECT * FROM delta_scan('gs://northeastern-pdf-ndas/db/parties');")
    con.execute("CREATE OR REPLACE VIEW risks AS SELECT * FROM delta_scan('gs://northeastern-pdf-ndas/db/risks');")
    con.execute(
        "CREATE OR REPLACE VIEW milestones AS SELECT * FROM delta_scan('gs://northeastern-pdf-ndas/db/milestones');"
    )
    return con


def launch_duckdb_ui():
    """Launch duckdb UI with delta connection."""
    conn = confiure_duckdb_gcs_delta()
    conn.execute("CALL start_ui()")


def get_risk_analysis() -> pl.DataFrame:
    """Analyzes the relationship between NDA agreement types and their risk profiles.

    This analysis helps legal teams understand which types of NDAs (Mutual vs. Unilateral)
    tend to carry higher legal risks. It calculates the percentage of agreements with
    high-severity risks for each agreement type, along with the average confidentiality
    period. This information can guide resource allocation for legal review and risk
    mitigation, allowing teams to focus more attention on agreement types that
    historically present greater legal exposure.

    Returns:
        DataFrame containing agreement types, risk counts, and risk percentages
    """
    conn = configure_duckdb_gcs_delta()
    with open(SQLS / "RISK_ANALYSIS.sql") as f:
        sql = f.read()
    return conn.query(sql).pl()


def get_timeline_analysis() -> pl.DataFrame:
    """Examines the timeline structure of NDAs across different governing jurisdictions.

    This analysis tracks the time intervals between the effective date and key milestones
    in each agreement, grouped by governing law. It helps business and legal teams
    understand typical timeline patterns in different jurisdictions, which is valuable for
    contract planning, compliance tracking, and understanding regional variations in
    agreement structures. The analysis reveals which jurisdictions tend to have longer
    or shorter contractual timelines, supporting better forecasting of obligations
    and expiration dates.

    Returns:
        DataFrame containing milestone timelines grouped by governing jurisdiction
    """
    conn = configure_duckdb_gcs_delta()
    with open(SQLS / "TIMELINE_ANALYSIS.sql") as f:
        sql = f.read()
    return conn.query(sql).pl()


def get_party_risk_correlation() -> pl.DataFrame:
    """Identifies correlations between party relationships and risk levels in NDAs.

    This analysis examines how the combination of different parties, their roles
    (disclosing vs. receiving), and their relationships correlates with risk levels
    in agreements. It helps organizations understand which party configurations tend
    to create higher-risk scenarios, enabling more informed decisions about when to
    apply additional scrutiny or negotiation effort. The results can guide strategic
    approaches to different counterparties based on historical risk patterns and
    allow legal teams to develop targeted risk mitigation strategies for specific
    party relationships.

    Returns:
        DataFrame showing relationships between party configurations and risk levels
    """
    conn = configure_duckdb_gcs_delta()
    with open(SQLS / "PARTY_RISK_CORRELATION.sql") as f:
        sql = f.read()
    return conn.query(sql).pl()
