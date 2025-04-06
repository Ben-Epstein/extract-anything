import json
import os

from dotenv import find_dotenv, set_key
from google.cloud import storage

from shared import GOOGLE_APPLICATION_CREDENTIALS

_GOOGLE_CLOUD_HMAC_KEY_ID = "GOOGLE_CLOUD_HMAC_KEY_ID"
_GOOGLE_CLOUD_HMAC_SECRET = "GOOGLE_CLOUD_HMAC_SECRET"


def _build_hmac_keys(project_id: str, service_account_email: str, save: bool = False) -> tuple[str, str]:
    storage_client = storage.Client(project=project_id)

    hmac_key, secret = storage_client.create_hmac_key(
        service_account_email=service_account_email, project_id=project_id
    )
    if save and (path := find_dotenv()):
        set_key(path, _GOOGLE_CLOUD_HMAC_KEY_ID, str(hmac_key.access_id))
        set_key(path, _GOOGLE_CLOUD_HMAC_SECRET, secret)
    return str(hmac_key.access_id), secret


def get_hmac_keys() -> tuple[str, str]:
    """Retrieves the access key and secret key for the service account specified.

    Will look for values in the following order:
        * GOOGLE_CLOUD_HMAC_KEY_ID and GOOGLE_CLOUD_HMAC_SECRET env vars
        * GOOGLE_CLOUD_PROJECT and GOOGLE_CLOUD_SERVICEACCOUNT env vars
        * GOOGLE_APPLICATION_CREDENTIALS environment variable.

    Returns:
        tuple: (access_key, secret_key)
    """
    if (hmac_key := os.getenv(_GOOGLE_CLOUD_HMAC_KEY_ID)) and (hmac_secret := os.getenv(_GOOGLE_CLOUD_HMAC_SECRET)):
        return hmac_key, hmac_secret
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    service_account_email = os.getenv("GOOGLE_CLOUD_SERVICEACCOUNT")
    if project_id and service_account_email:
        return _build_hmac_keys(project_id, service_account_email, save=True)

    if not GOOGLE_APPLICATION_CREDENTIALS:
        raise RuntimeError(
            "Must have (GOOGLE_CLOUD_PROJECT and GOOGLE_CLOUD_SERVICEACCOUNT) set, or GOOGLE_APPLICATION_CREDENTIALS"
        )
    print("No env vars found, using GOOGLE_APPLICATION_CREDENTIALS")
    with open(GOOGLE_APPLICATION_CREDENTIALS, "r") as f:
        credentials_info = json.load(f)
        service_account_email = credentials_info.get("client_email")
        project_id = credentials_info.get("project_id")

    if not service_account_email or not project_id:
        raise ValueError("Invalid service account key file.")
    return _build_hmac_keys(project_id, service_account_email, save=True)
