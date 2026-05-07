from fastapi import FastAPI

from app.checker import test_oci_connection

app = FastAPI()


@app.get("/")
def root():
    return {
        "message": "OCI ARM Monitor Running"
    }


@app.get("/test-oci")
def test_oci():
    return test_oci_connection()