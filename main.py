from fastapi import FastAPI

app = FastAPI()

@app.get("/welcome")

def welcome():
    return{
        "message": "Hello World"
    }


# uvicorn main:app --reload --host 0.0.0.0 --port 8000