from fastapi import FastAPI
app = FastAPI()
@app.get("/")
def home():
    return {"message": "Welcome to FastAPI"}

@app.get("/name")
def name():
    return {"name": "Amarah Mir"}

