from datetime import datetime
from sqlite3 import Timestamp
from pydantic import BaseModel
from typing import List

from db.models import User

class UserBase(BaseModel):
    username: str
    email: str
    password: str

class UserDisplay(BaseModel):
    username: str
    email:str

    class Config():
        orm_mode = True

class PostBase(BaseModel):
    image_url: str
    image_url_type: str
    caption: str
    creator_id: int

# for Post Display
class User(BaseModel):
    username: str
    class Config():
        orm_mode = True

# for PostDisplay
class Comment(BaseModel):
    user_comment: str
    username: str
    timestamp: datetime
    class Config():
        orm_mode = True


class PostDisplay(BaseModel):
    id: int
    image_url: str
    image_url_type: str
    caption: str
    timestamp: datetime
    user: User
    comments: List[Comment]

    class Config():
        orm_mode = True

class UserAuth(BaseModel):
    id: int
    username: str
    email: str

class CommentBase(BaseModel):
    username: str
    user_comment: str
    post_id: int
