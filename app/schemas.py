from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class UserOut(BaseModel):
    id: int
    email: str
    username: str
    is_pro: bool
    created_at: datetime
    class Config:
        from_attributes = True

class LinkCreate(BaseModel):
    url: str
    custom_slug: Optional[str] = None

class LinkOut(BaseModel):
    id: int
    slug: str
    original_url: str
    clicks: int
    created_at: datetime
    class Config:
        from_attributes = True

class LinkDetail(LinkOut):
    short_url: str

class SubscribeRequest(BaseModel):
    plan: str
