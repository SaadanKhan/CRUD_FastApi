from fastapi import FastAPI,Response,status,HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange


app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello World"}


@app.get("/post")
def posts():
    return {"POSTS": posts}

class Post(BaseModel):
       title : str
       content : str
       published: bool = True
       rating: Optional[int] = None    


# Our small database
posts = []

def delete(id):
    for i,p in enumerate(posts):
        if p['id'] == id:
            return i


def get_post_by_id(id):
    for p in posts:
        if p['id'] == id:
            return p


@app.post("/post",status_code=status.HTTP_201_CREATED)
def create_post(post:Post):
       post_dict = post.dict()
       post_dict['id'] = randrange(0,100)
       posts.append(post_dict)
       return post_dict


@app.get("/post/latest")
def get_latest_post():
    post = posts[len(posts)-1]
    return {"Latest Post": post}


@app.get("/post/{id}")
def get_post(id:int):
    post = get_post_by_id(id)
    
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f" post with the id: {id} not found"
            )

    return {"Your post": post}



@app.delete("/post/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int):
    post = delete(id)
    
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with the id: {id} does not exists...")

    posts.pop(post)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/post/{id}")
def update_post(id:int,post:Post):

    post_id = delete(id)
    if post_id == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with the id: {id} does not exists...")

    # Taking the post from the front-end and converting it to dict
    post_dict = post.dict() 
    post_dict["id"] = id
    posts[post_id] = post_dict

    return {"data":post_dict}