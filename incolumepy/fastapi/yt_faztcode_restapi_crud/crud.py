from urllib import response
from fastapi import FastAPI, HTTPException, status, Response
from pydantic import BaseModel
from typing import Optional, Text
from datetime import datetime
from uuid import uuid4 as uuid
import uvicorn

app = FastAPI()

posts = []

# Post model
class Post(BaseModel):
    id: Optional[str]
    title: str
    author: str
    content: Text
    created_at: datetime =  datetime.now()
    published_at: Optional[datetime]
    published: Optional[bool] = False

@app.get('/')
def read_root():
    return {"detail": "Welcome to my API"}

@app.get('/posts')
def get_posts():
    return posts

@app.post('/posts', status_code=status.HTTP_201_CREATED)
def save_post(post: Post):
    post.id = str(uuid())
    posts.append(post.dict())
    return posts[-1]

@app.get('/posts/{post_id}')
def get_post(post_id: str):
    for post in posts:
        if post["id"] == post_id:
            return post
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")

@app.delete('/posts/{post_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: str, resp: Response):
    for index, post in enumerate(posts):
        if post["id"] == post_id:
            posts.pop(index)
            resp.status_code = status.HTTP_204_NO_CONTENT
            return {"message": "Post has been deleted succesfully"}
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Item not found")

@app.put('/posts/{post_id}', status_code=status.HTTP_202_ACCEPTED)
def update_post(post_id: str, updatedPost: Post, resp: Response):
    for index, post in enumerate(posts):
        if post["id"] == post_id:
            posts[index]["title"]= updatedPost.dict()["title"]
            posts[index]["content"]= updatedPost.dict()["content"]
            posts[index]["author"]= updatedPost.dict()["author"]
            resp.status_code = status.HTTP_202_ACCEPTED
            return {"message": "Post has been updated succesfully"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")


