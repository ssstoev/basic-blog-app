from fastapi import FastAPI

# we import the root from the route file we created
from routes.entry import entry_root
from routes.blog import blog_root

app = FastAPI()

# this includes the API router we created in entry.py
app.include_router(entry_root)
app.include_router(blog_root)