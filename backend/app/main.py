from fastapi import FastAPI, HTTPException, status, Depends
from app.schemas import PostCreate, PostResponse, PostUpdate
from datetime import datetime
from app.database import engine, Base, get_db
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models import Post as PostModel
from fastapi.middleware.cors import CORSMiddleware

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
app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/posts", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
async def create_post(post: PostCreate, db: Session = Depends(get_db)):

    db_post = PostModel(**post.model_dump())
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

@app.get("/posts", response_model=list[PostResponse], status_code=status.HTTP_200_OK)
async def get_posts(db: Session = Depends(get_db)):
    posts = db.scalars(select(PostModel)).all()
    return posts

@app.get("/posts/{post_id}", response_model=PostResponse, status_code=status.HTTP_200_OK)
async def get_post(post_id: int, db: Session = Depends(get_db)):

    post = db.scalars(select(PostModel).where(PostModel.id == post_id)).first()
    if not post: raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return post

@app.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(post_id: int, db: Session = Depends(get_db)):

    post = db.scalars(select(PostModel).where(PostModel.id == post_id)).first()
    if not post: raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    db.delete(post)
    db.commit()

@app.patch("/posts/{post_id}", response_model=PostResponse, status_code=status.HTTP_200_OK)
async def update_post(post_id: int, post_update: PostUpdate, db: Session = Depends(get_db)):

    post = db.scalars(select(PostModel).where(PostModel.id == post_id)).first()
    if not post: raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    update_data = post_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(post, key, value)

    db.commit()
    db.refresh(post)
    return post






