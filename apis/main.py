# fastapi_app/main.py
# database name is - ganeshaidol , port num is 5432, username is postgres , password is postgres
from fastapi import FastAPI, Depends, Request, HTTPException

from fastapi.responses import JSONResponse

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from db.database import SessionLocal, engine, insert_user
from db.base import Base
from pymodels.models import User, Event
from redis import Redis
app = FastAPI()

redis_client = Redis(host="localhost", port=6379, db=0, decode_responses=True)
RATE_LIMIT = 5000
TIME_WINDOW = 60
app = FastAPI()

def get_ip_client(request):
    return request.client.host

@app.post("/eventprocessor")
async def event_processor(event: Event):
    return {"eventname": event.event_name, "eventstatus": event.event_status, "eventvalid": event.valid}


@app.middleware("http")
async def rate_limiter(request: Request, call_next):
    ip = get_ip_client(request)
    key = f"client: {ip}"
    current = redis_client.get(key)
    if current is None:
        redis_client.set(key, 1, ex=TIME_WINDOW)
    elif int(current) < RATE_LIMIT:
        redis_client.incr(key)
    else:
        ttl = redis_client.ttl(key)
        return JSONResponse(
            status_code=429,
            content={"detail": f"Throttled, too many requests try after {ttl} seconds"}
        )
    print("forwarding the request")
    response = await call_next(request)
    print("getting the request")
    return response

# Create DB tables on startup
@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# to push the record you need session object

@app.post("/user")
async def add_user(user: User):
    # the  user from request is json , fast api converted to pydantic model
    user_data = user.dict()
    return await insert_user(user_data)


