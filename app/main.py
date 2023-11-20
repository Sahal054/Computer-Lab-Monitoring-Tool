from fastapi import FastAPI
from db.database import engine
from models import models



app = FastAPI()

models.Base.metadata.create_all(bind=engine)

@app.get("/")
async def test():

    return {"message":"hello"}
