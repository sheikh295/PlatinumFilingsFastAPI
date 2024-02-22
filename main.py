from typing import Union, List, Optional
from typing_extensions import Annotated
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
import models
from db import engine, SessionLocal
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title= "Platinum Filings API",
    description= "An API for accessing Florida filing data",
    version="1.0.0"
)
models.Base.metadata.create_all(bind=engine)

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:5173",
    "https://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#Creat your Schema Here
class Item(BaseModel):
    id: int
    fei_no: Optional[int] = None
    address: str
    registered_agent: bool
    agent_name: str
    agent_address: str
    authorized_manager: str
    authorized_manager_two: Optional[str] = None
    authorized_manager_three: Optional[str] = None
    name: str
    email: str
    phone_no: Optional[int] = None
    certificate: Optional[bool] = None
    signing_officer_name: str
    signing_officer_signature: str
    signing_officer_title: str
    business_entity: str

    class Config:
        orm_mode = True

def getDB():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependancy = Annotated[Session, Depends(getDB)]

@app.get("/")
def root():
    return {"Hello": "Welcome to FAST API"}

@app.post("/data")
async def createUser(user: Item, db: db_dependancy):
    try:
        UserData = models.Users(id=user.id, fei_no=user.fei_no, address=user.address, registered_agent=user.registered_agent, agent_name=user.agent_name, agent_address=user.agent_address, authorized_manager=user.authorized_manager, authorized_manager_two=user.authorized_manager_two, authorized_manager_three=user.authorized_manager_three, name=user.name, email=user.email, phone_no=user.phone_no, certificate=user.certificate, signing_officer_name=user.signing_officer_name, signing_officer_signature=user.signing_officer_signature, signing_officer_title=user.signing_officer_title, business_entity=user.business_entity)
        db.add(UserData)
        db.commit()
        db.refresh(UserData)
        return {"Status": "Success", "Data": UserData}
    except Exception as e:
        return {"Status": "Failed", "Error": str(e)}
    
@app.get("/getById/{user_id}")
async def getById(db: db_dependancy, user_id: int):
    result = db.query(models.Users).filter(models.Users.id == user_id).first()
    if not result:
        raise HTTPException(status_code=404, detail="Could not find user")
    else:
        return result