from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.enums import PostType


class Post(BaseModel):
    title: str
    body: str
    tags: list[PostType]


class PostCreate(Post):
    pass


class PostResponse(Post):
    id: int
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)


class PostUpdate(BaseModel):
    title: str | None = None
    body: str | None = None
    tag: str | None = None


class PaginatedPostResponse(BaseModel):
    items: list[PostResponse]
    total: int
    page: int
    limit: int
    total_pages: int
