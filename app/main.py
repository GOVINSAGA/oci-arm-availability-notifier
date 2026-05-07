from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def root():
    return {
        "message": "OCI ARM Monitor Running"
    }