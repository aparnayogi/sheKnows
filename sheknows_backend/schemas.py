from pydantic import BaseModel
from datetime import date
from typing import Optional

class UserSignUp(BaseModel):
    first_name : str
    last_name : str
    email :str
    mobile_no :int
    password: str
    city:str
    
    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

class LoginForUser(BaseModel):
    user_email : str
    password : str
    
    class Config:
        orm_mode = True
        arbitrary_types_allowed = True