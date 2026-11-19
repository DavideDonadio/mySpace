from fastapi import FastAPI, HTTPException, status
from app.schemas import PostCreate, PostResponse, PostUpdate
from datetime import datetime

app = FastAPI()

fake_db = []

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/posts", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
async def create_post(post: PostCreate):

    post_dict = post.model_dump()
    post_dict["id"] = len(fake_db) + 1
    post_dict["created_at"] = datetime.now()
    post_dict["updated_at"] = datetime.now()
    fake_db.append(post_dict)
    return post_dict

@app.get("/posts", response_model=list[PostResponse], status_code=status.HTTP_200_OK)
async def get_posts():
    return fake_db

@app.get("/posts/{post_id}", response_model=PostResponse, status_code=status.HTTP_200_OK)
async def get_post(post_id: int):

    for post in fake_db:
        if post["id"] == post_id:
            return post
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

@app.delete("/posts/{post_id}", response_model=PostResponse, status_code=status.HTTP_200_OK)
async def delete_post(post_id: int):

    for post in fake_db:
        if post["id"] == post_id:
            fake_db.remove(post)
            return post

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

@app.patch("/posts/{post_id}", response_model=PostResponse, status_code=status.HTTP_200_OK)
async def update_post(post_id: int, post_update: PostUpdate):

    post_dict = post_update.model_dump(exclude_unset=True)
    for post in fake_db:
        if post["id"] == post_id:
            post.update(post_dict)
            post["updated_at"] = datetime.now()
            return post

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)





