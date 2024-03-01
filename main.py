from typing import Union, List, Optional
from typing_extensions import Annotated
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
import models
from db import engine, SessionLocal
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from aiocache import caches, SimpleMemoryCache
from aiocache.serializers import PickleSerializer
from aiocache.decorators import cached
import json
from fastapi.responses import StreamingResponse


cache = caches.get("default")
if cache is None:
    cache = SimpleMemoryCache(serializer=PickleSerializer)
    caches.set("default", cache)


app = FastAPI(
    title= "Platinum Filings API",
    description= "An API for accessing Florida filing data",
    version="1.0.0"
)
models.Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://phpstack-961691-4302635.cloudwaysapps.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Item(BaseModel):
    id: Optional[int] = None
    Corporation_Number: str
    Corporation_Name: str
    Status: str
    Filing_Type: str
    Address_1: str
    Address_2: str
    City: str
    State: str
    Zip: str
    Country: Optional[str] = None
    Mail_Address_1: str
    Mail_Address_2: str
    Mail_City: str
    Mail_State: str
    Mail_Zip: str
    Mail_Country: Optional[str] = None
    File_Date: str
    FEI_Number: str
    More_than_six_Officers_flag: str
    Last_Transaction_Date: str
    State_Country: str
    Report_Year_1: str
    Filler1: str
    Report_Date_1: str
    Report_Year_2: str
    Filler2: str
    Report_Date_2: str
    Report_Year_3: str
    Filler3: str
    Report_Date_3: str
    Registered_Agent_Name: str
    Registered_Agent_Type: str
    Registered_Agent_Address: str
    Registered_Agent_City: str
    Registered_Agent_State: str
    Registered_Agent_Zip_plus_4: Optional[str] = None
    Officer_1_Title: str
    Officer_1_Type: str
    Officer_1_Name: str
    Officer_1_Address: str
    Officer_1_City: str
    Officer_1_State: str
    Officer_1_Zip_plus_4: Optional[str] = None
    Officer_2_Title: str
    Officer_2_Type: str
    Officer_2_Name: str
    Officer_2_Address: str
    Officer_2_City: str
    Officer_2_State: str
    Officer_2_Zip_plus_4: Optional[str] = None
    Officer_3_Title: Optional[str] = None
    Officer_3_Type: Optional[str] = None
    Officer_3_Name: Optional[str] = None
    Officer_3_Address: Optional[str] = None
    Officer_3_City: Optional[str] = None
    Officer_3_State: Optional[str] = None
    Officer_3_Zip_plus_4: Optional[str] = None
    Officer_4_Title: Optional[str] = None
    Officer_4_Type: Optional[str] = None
    Officer_4_Name: Optional[str] = None
    Officer_4_Address: Optional[str] = None
    Officer_4_City: Optional[str] = None
    Officer_4_State: Optional[str] = None
    Officer_4_Zip_plus_4: Optional[str] = None
    Officer_5_Title: Optional[str] = None
    Officer_5_Type: Optional[str] = None
    Officer_5_Name: Optional[str] = None
    Officer_5_Address: Optional[str] = None
    Officer_5_City: Optional[str] = None
    Officer_5_State: Optional[str] = None
    Officer_5_Zip_plus_4: Optional[str] = None
    Officer_6_Title: Optional[str] = None
    Officer_6_Type: Optional[str] = None
    Officer_6_Name: Optional[str] = None
    Officer_6_Address: Optional[str] = None
    Officer_6_City: Optional[str] = None
    Officer_6_State: Optional[str] = None
    Officer_6_Zip_plus_4: Optional[str] = None
    Filler4: str

    class Config:
        orm_mode = True

def getDB():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(getDB)]

@app.get("/")
def root():
    return {"Hello": "Welcome to FAST API"}

@app.get("/healthCheck")
def healthCheck():
    return {"Health Status": "OKAY"}

#--------------Below Two Routes are for Debugging Purposes------------------#

# @app.get("/getsqlalchemy")
# async def getOne(db: db_dependency):
#     result = db.query(models.Cordataq4).limit(5).all()
#     return result


# @app.get("/getsqlraw")
# async def getAll(db: db_dependency):
#     try:
#         query = text(f"SELECT * FROM cordataq4 LIMIT 5")
#         result = db.execute(query)
        
#         column_names = result.keys()
        
#         rows = result.fetchall()
        
#         if rows:
#             data = []
#             for row in rows:
#                 row_dict = dict(zip(column_names, row))
#                 data.append(row_dict)
#             return data
#         else:
#             raise HTTPException(status_code=404, detail="No data found")
#     except HTTPException:
#         raise
#     except Exception as e:
#         print(f"An error occurred: {e}")
#         raise HTTPException(status_code=500, detail="Internal server error")
    
    
@app.get("/getById/{user_id}", response_model=Item)
async def get_by_id(user_id: int, db: db_dependency):
    data = db.query(models.Cordataq4).filter_by(id = user_id).first()
    if not data:
        raise HTTPException(status_code=404, detail="No data found")
    return data


@app.put("/updateById/{user_id}")
async def update_by_id(user_id: int, update_data: Item, db: db_dependency):
    try:
        db_data = db.query(models.Cordataq4).filter(models.Cordataq4.id == user_id).first()
    except:
        error = "incorrect Id"
        return error
    if not db_data:
        raise HTTPException(status_code=404, detail="Data not found")
    
    for key, value in update_data.model_dump(exclude={"id"}).items():
        setattr(db_data, key, value)
    
    db.commit()
    db.refresh(db_data)
    return {"message": "Data updated successfully"}


@app.post("/addData")
async def add_data(item: Item, db: db_dependency):
    try:
        new_data = models.Cordataq4(**item.model_dump(exclude={"id"}))
        db.add(new_data)
        db.commit()
        db.refresh(new_data)
        return {"message": "Data added successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to add data: {str(e)}")