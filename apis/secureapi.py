from fastapi import FastAPI
from datetime import datetime, timedelta
from jose import jwt
from pydantic import BaseModel
from passlib.context import CryptContext

class LoginRequest(BaseModel):
    username: str
    password: str



from passlib.context import CryptContext

app = FastAPI()
pwd_context = CryptContext(schemes=("bcrypt"), deprecated="auto")
fake_db = {'alice':{'username':'alice','password':pwd_context.hash("secure123")}}

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def verify_user(user: str):
    if fake_db['alice']['username']==user:
        return user
    return None

SECRET_KEY = "mysecret"
ALGORITHM = "HS256" # RS256 is recommended , this is training purpose
ACCESS_TOKEN_EXPIRY_MINUTES = 30

def access_token(user: str ):
    payload = {'username': user, 'exp':ACCESS_TOKEN_EXPIRY_MINUTES}
    token = jwt.encode(payload, SECRET_KEY, algorithm = ALGORITHM)
    return token



@app.post("/login")
async def login(credentials: LoginRequest):
    user = verify_user(credentials.username)
    if not user or not verify_password(credentials.password, fake_db['alice']['password']):
        return None
    return access_token(user)
