""" import modules"""
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

import models
from connections import schema,crud
from connections.database import engine, get_db
from security.jwt_bearer import JWTBearer
from security.jwt_handler import signJWT_access, signJWT_refresh, decodeJWT

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

@app.get('/')
async def root():
    """ sample function """
    return {"Message":"Hello World"}


@app.post("/createemp")
async def create_employee(emp:schema.EmployeeData,db_data: Session = Depends(get_db)):
    """ create new employee """
    user_name = crud.get_user_by_username(db_data=db_data,username=emp.username)
    user_email = crud.get_user_by_email(db_data=db_data,email=emp.email)
    user_phone = crud.get_user_by_phonenumber(db_data=db_data,phonenumber=emp.phonenumber)

    if user_name:
        return {"message":"username already exist"}
    if user_email:
        return {"message":"Email already exist"}
    if user_phone:
        return {"message":"Phonenumber already exist"}

    crud.create_employee(db_data=db_data,emp=emp)
    return {"Status":200,"Message":"Employee created successfully"}



@app.post("/emaillogin")
async def email_password_login(email:str,password:str,db_data:Session = Depends(get_db)):
    """ employee login by email and password """
    emp_data = crud.verify_emp_by_email_password(db_data=db_data, email=email, password=password)
    if emp_data:
        access_jwt_token = signJWT_access(emp_data.phonenumber)
        refresh_jwt_token = signJWT_refresh(emp_data.phonenumber)

        return ({"status_code": 200, 'Status': 'Success', 'Message': 'Login Success',
                 "access_jwt_token": access_jwt_token, "refresh_jwt_token": refresh_jwt_token})

    user_email = crud.get_user_by_email(db_data=db_data, email=email)
    if not user_email:
        return {"status_code":200,"status":"Error","Message":"Employee not found"}

    return {"status_code":200,"status":"Error","Message":"Invalid credentials"}


@app.get('/getemployee',dependencies=[Depends(JWTBearer())])
async def get_logined_emp(db_data:Session = Depends(get_db),token: str = Depends(JWTBearer())):
    """ get logined employee data"""
    decodedata = decodeJWT(token)
    user_exists = crud.get_user_by_phonenumber(db_data=db_data, phonenumber=decodedata['mobile_number'])
    if user_exists:
        return user_exists
    return {"Employee details not found"}



