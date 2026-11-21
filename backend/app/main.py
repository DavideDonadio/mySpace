import math

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import desc, func, select
from sqlalchemy.orm import Session

from app.database import Base, engine, get_db
from app.models import Post as PostModel
from app.schemas import PaginatedPostResponse, PostCreate, PostResponse, PostUpdate

app = FastAPI()

# Allow requests from your Astro dev server
origins = [
    "http://localhost:4321",
    "http://127.0.0.1:4321",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)


@app.post("/posts", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
async def create_post(post: PostCreate, db: Session = Depends(get_db)):

    db_post = PostModel(**post.model_dump())
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


@app.get("/posts", response_model=PaginatedPostResponse, status_code=status.HTTP_200_OK)
async def get_posts(db: Session = Depends(get_db), page: int = 1, limit: int = 10):

    tot_posts = db.scalar(select(func.count()).select_from(PostModel)) or 0
    offset = (page - 1) * limit

    query = (
        select(PostModel)
        .order_by(desc(PostModel.created_at))
        .offset(offset)
        .limit(limit)
    )
    posts = db.scalars(query).all()
    tot_pages = math.ceil(tot_posts / limit)
    return PaginatedPostResponse(
        items=posts, page=page, limit=limit, total_pages=tot_pages, total=tot_posts
    )


@app.get(
    "/posts/{post_id}", response_model=PostResponse, status_code=status.HTTP_200_OK
)
async def get_post(post_id: int, db: Session = Depends(get_db)):

    post = db.scalars(select(PostModel).where(PostModel.id == post_id)).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return post


@app.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(post_id: int, db: Session = Depends(get_db)):

    post = db.scalars(select(PostModel).where(PostModel.id == post_id)).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    db.delete(post)
    db.commit()


@app.patch(
    "/posts/{post_id}", response_model=PostResponse, status_code=status.HTTP_200_OK
)
async def update_post(
    post_id: int, post_update: PostUpdate, db: Session = Depends(get_db)
):

    post = db.scalars(select(PostModel).where(PostModel.id == post_id)).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    update_data = post_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(post, key, value)

    db.commit()
    db.refresh(post)
    return post
