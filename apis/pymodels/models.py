from pydantic import BaseModel
class Event(BaseModel):
    event_name: str
    event_status: str
    valid: bool

class User(BaseModel):
    name: str
    email: str