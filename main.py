from fastapi import FastAPI
from pydantic import BaseModel
from tables import create_tables
from verify import create_user, verify_user

app = FastAPI()

create_tables()

class User(BaseModel):
    username: str
    password: str


@app.get("/")
def home():
    return {"message": "API is running sucksexfully"}


@app.post("/register")
def register(user: User):
    return {"message": create_user(user.username, user.password)}


@app.post("/login")
def login(user: User):
    db_user = verify_user(user.username, user.password)

    if db_user:
        return {"message": "Login successful"}

    return {"message": "ille podde"}