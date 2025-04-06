import duckdb
from shared.gcs import get_hmac_keys


def authenticate_gcs_delta_duckdb():
    key, secret = get_hmac_keys()
    duckdb.execute(f"""
    CREATE OR REPLACE SECRET (
        TYPE gcs,
        KEY_ID '{key}',
        SECRET '{secret}'
    );
    """)
