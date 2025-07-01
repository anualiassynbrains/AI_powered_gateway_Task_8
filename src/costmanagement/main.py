import os
from fastapi import FastAPI,HTTPException,Depends,status
from pydantic import BaseModel
from typing import Annotated, Optional
from phase1.summarizer import summarize_text
from redis.asyncio import Redis
from auth.rate_limiter import redis,cost_based_limiter


app=FastAPI()
@app.on_event("startup")
async def startup_event():
    await redis.ping()

@app.on_event("shutdown")
async def shutdown_event():
    await redis.close()

class Textdata(BaseModel):
    text:str


cost_dependency=Annotated[dict,Depends(cost_based_limiter)]

@app.post('/summarize',status_code=status.HTTP_200_OK)
async def summarize(textdata:Textdata,costdepend:cost_dependency):
    data=await summarize_text(textdata.text)
    if data:
        return {
            "summary": data,
            "cost": costdepend["cost"],
            "remaining_credits": costdepend["remaining_credits"]
        }
    else:
        raise HTTPException(status_code=404,detail='didnt get the data')
