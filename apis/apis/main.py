# fastapi_app/main.py
# database name is - ganeshaidol , port num is 5432, username is postgres , password is postgres
from fastapi import FastAPI, Depends, Request, HTTPException

from fastapi.responses import JSONResponse

# from sqlalchemy.ext.asyncio import AsyncSession
# from sqlalchemy import text
# from .db.database import SessionLocal, engine, Base
# from .db.models import User
# from redis import Redis

///
redis_client = Redis(host="localhost", port=6379, db=0, decode_responses=True)
RATE_LIMIT = 5
TIME_WINDOW = 60
app = FastAPI()

def get_ip_client(request):
    return request.client.host


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

    response = await call_next(request)
    return response


///



@app.get("/p")
def read_root():
    return {"message": "Hello, FastAPI with Poetry!"}
///

@app.get("/item/{item}")
def get_item(item):
    return (f"string is returned {item}")


# Create DB tables on startup
@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Dependency to get DB session
async def get_db():
    async with SessionLocal() as session:
        yield session

@app.get("/")
async def read_users(db: AsyncSession = Depends(get_db)):
    result = await db.execute(text("SELECT * FROM users"))
    rows = result.fetchall()
    columns = result.keys()
    users = [dict(zip(columns, row)) for row in rows]
    return users

@app.get("/test429")
async def test():
    raise HTTPException(status_code=429, detail="Too many requests")

///




@app.get("/ph")
def read_root():
    return {"message": "Hello, FastAPI with Poetrpy!"}
