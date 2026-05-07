import time
import sys


sys.stdout.reconfigure(line_buffering=True)

from app.checker import auto_create_arm_instance


while True:
    print("Checking ARM availability...", flush=True)

    result = auto_create_arm_instance()

    print(result, flush=True)

    if result.get("created"):
        print("ARM instance successfully created!")
        break

    reason = result.get("reason")

    if reason == "RATE_LIMITED":
        print("OCI rate limited requests. Sleeping 10 minutes...", flush=True)
        time.sleep(600)

    elif reason == "NETWORK_ERROR":
        print("Temporary network issue. Sleeping 5 minutes...", flush=True)
        time.sleep(300)

    else:
        print("ARM capacity unavailable. Retrying in 3 minutes...", flush=True)
        time.sleep(180)