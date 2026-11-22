import math
from datetime import timedelta

from fastapi import HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import desc, func, select
from sqlalchemy.orm import Session

from app.database import Base, engine, get_db
from app.models import Post as PostModel
from app.models import User as UserModel
from app.schemas import PaginatedPostResponse, PostCreate, PostResponse, PostUpdate, Token, UserResponse, UserCreate
from app import auth

from typing import Annotated
from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


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
async def create_post(curr_user: Annotated[UserModel, Depends(auth.get_current_user)], post: PostCreate, db: Session = Depends(get_db)):

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
async def delete_post(curr_user: Annotated[UserModel, Depends(auth.get_current_user)], post_id: int, db: Session = Depends(get_db)):

    post = db.scalars(select(PostModel).where(PostModel.id == post_id)).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    db.delete(post)
    db.commit()

@app.patch(
    "/posts/{post_id}", response_model=PostResponse, status_code=status.HTTP_200_OK
)
async def update_post(curr_user: Annotated[UserModel, Depends(auth.get_current_user)],
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

@app.post("/auth/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_in: UserCreate, db: Session = Depends(get_db)):

    existing_user = db.scalars(select(UserModel).where(UserModel.username == user_in.username)).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    hashed_pw = auth.get_password_hash(user_in.password)
    new_user = UserModel(username = user_in.username, hashed_password= hashed_pw)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.post("/token")
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)) -> Token:

    username = form_data.username
    user = db.scalars(select(UserModel).where(UserModel.username == username)).first()

    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    return Token(access_token=access_token, token_type="bearer")
