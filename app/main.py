from fastapi import FastAPI

from app.checker import (
    test_oci_connection,
    check_arm_shapes
)

app = FastAPI()


@app.get("/")
def root():
    return {
        "message": "OCI ARM Monitor Running"
    }


@app.get("/test-oci")
def test_oci():
    return test_oci_connection()


@app.get("/check-arm")
def check_arm():
    return check_arm_shapes()