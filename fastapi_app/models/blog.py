from pydantic import BaseModel
from typing import List, Optional
# we create our blog object which we will be using to create and modify blogs

# Idea: add a comment section 

# Note: no need to store dates since it will be done autoatically
class BlogModel(BaseModel):
    title: str
    sub_title: str 
    content: str
    author: Optional[str] = None
    tags: Optional[list] = None

class UpdateBlogModel(BaseModel):
    title: str = None
    sub_title: str = None
    content: str = None
    author: str = None
    tags: list = None