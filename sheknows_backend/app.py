from fastapi import FastAPI
from fastapi import Request
import json
import backend_db as fsd_db
from typing import Dict
from fastapi.responses import JSONResponse
import schemas

app = FastAPI()

@app.get("/")
def read_root():
 return {"message": "Hello, FastAPI!"}

@app.post("/user_signup")
def user_signup(signup_details:schemas.UserSignUp):
    print(signup_details)
    result = fsd_db.user_signup(signup_details.dict())
    response = {
        "data" : result
    }
    return JSONResponse(content=response)

@app.post("/attempt_to_login_for_user")
def attempt_to_login_for_user(login_data:schemas.LoginForUser):
    valid_user_login = ""
    valid_user = fsd_db.validate_login_details(login_data.dict())
    if(valid_user):
        valid_user_login = "Login Successful"
    else:
        valid_user_login = "Login Failed"

    response = {
        "status" : valid_user_login
    }
    return JSONResponse(content=response, status_code=200)