from fastapi import FastAPI

app = FastAPI(title="City Climate Explorer")

@app.get("/")
def root():
    return {"message": "City Climate Explorer API"}