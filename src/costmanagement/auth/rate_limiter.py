import asyncio
import os
import sys
from fastapi import Request, Header, HTTPException
from redis.asyncio import Redis
from phase1.costestimator import estimate_cost_request
from phase1.summarizer import summarize_text
from dotenv import load_dotenv
load_dotenv()


REDIS_URL = os.getenv("REDIS_URL")
redis = Redis.from_url(REDIS_URL, decode_responses=True)

if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
async def cost_based_limiter(request: Request, x_api_key: str = Header(..., alias="X-API-Key")):
    user_credits=100
    user_key = f"user:{x_api_key}"
    try:
        body=await request.json()
        text=body.get('text','')
    except Exception as e:
        raise HTTPException(status_code=404,details='text is missing')
    balance = await redis.get(user_key)
    if balance is None:
        balance = user_credits
        await redis.set(user_key, user_credits)
    balance = int(balance)
    estimated_cost=await estimate_cost_request(text)
   
    if balance >= estimated_cost:
        await redis.decrby(user_key, estimated_cost)


    elif balance<estimated_cost:
        raise HTTPException(status_code=429,detail="Insufficient credits to process this request")
    

    return {
        "cost": estimated_cost,
        "remaining_credits": balance - estimated_cost
    }
    

