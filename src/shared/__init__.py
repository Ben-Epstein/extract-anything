"""A handful of libraries (cloudpathlib, baml) need env vars to be set before being imported, so we handle it here."""

import json
import os

from dotenv import load_dotenv
from prefect_gcp import GcpCredentials

res = load_dotenv()
if res:
    print("========= LOADED .env =========")
else:
    print("========= COULD NOT LOAD .env =========")


def set_google_creds():
    gcp_credentials_block: GcpCredentials = GcpCredentials.load("northeastern-gcs-bucket")  # type: ignore
    sa_file = "/tmp/google-serviceaccount.json"
    with open(sa_file, "w") as f:
        json.dump(gcp_credentials_block.service_account_info.get_secret_value(), f)  # type: ignore
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = sa_file


if not os.getenv("GOOGLE_APPLICATION_CREDENTIALS"):
    try:
        set_google_creds()
    except Exception:
        print("COULD NOT SET GOOGLE APPLICATION CREDENTIALS")


GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
