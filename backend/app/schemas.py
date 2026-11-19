from app.enums import PostType

from datetime import datetime
from pydantic import BaseModel, ConfigDict

class Post(BaseModel):
    title: str
    body: str
    tag: PostType

class PostCreate(Post):
    pass

class PostResponse(Post):
    id: int
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes = True)

