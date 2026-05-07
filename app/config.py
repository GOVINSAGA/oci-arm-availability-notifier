import os
from dotenv import load_dotenv

load_dotenv()

OCI_CONFIG = {
    "user": os.getenv("OCI_USER_OCID"),
    "key_file": os.getenv("OCI_KEY_FILE"),
    "fingerprint": os.getenv("OCI_FINGERPRINT"),
    "tenancy": os.getenv("OCI_TENANCY_OCID"),
    "region": os.getenv("OCI_REGION"),
    "compartment_id": os.getenv("OCI_COMPARTMENT_OCID"),
}