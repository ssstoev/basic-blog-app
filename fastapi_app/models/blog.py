from pydantic import BaseModel

# we create our blog object which we will be using to create and modify blogs

# Idea: add a comment section 

# Note: no need to store dates since it will be done autoatically
class BlogModel(BaseModel):
    title: str
    sub_title: str
    content: str
    author: str
    tags: list

class UpdateBlogModel(BaseModel):
    title: str = None
    sub_title: str = None
    content: str = None
    author: str = None
    tags: list = None