import datetime

from pydantic import BaseModel


class EmployeeData(BaseModel):
    username : str
    email : str
    password : str
    phonenumber:str
    role : str

class employee(EmployeeData):
    id: int
    created_date : datetime.datetime

    class Config:
        orm_mode = True