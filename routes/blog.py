from fastapi import APIRouter
from models.blog import BlogModel, UpdateBlogModel
import datetime as dt

#import the db collection
from config.config import blogs_collection

from serializers.blog import DecodeBlogs, DecodeBlog
from bson import ObjectId

blog_root = APIRouter()

# create a post request
@blog_root.post('/new/blog')

# we import the BlogModel class we created so that the input from the user matches this format
def NewBlog(data: BlogModel):
    data = dict(data) #convert the data to py dict

    current_date = dt.date.today()
    data['date'] = str(current_date)

    # add the new post to the DB
    response = blogs_collection.insert_one(data)

    # MongoDB automatically assigns an ID to every new element 
    # let's access this ID
    data_id = str(response.inserted_id)

    return {'status': 'ok', 
            'message': 'blog posted successfully in DB',
            '_id': data_id}

# getting Blogs
@blog_root.get("/all/blogs")
def AllBlogs():
    response = blogs_collection.find() # find() returns all the blogs
    decoded_data = DecodeBlogs(response)

    return {
        "status": "ok",
        "data": decoded_data
    }

# get blog with specific ID
@blog_root.get('/blog/{_id}')
def GetBlog(_id: str):
    response = blogs_collection.find_one({"_id": ObjectId(_id)})

    decoded_data = DecodeBlog(response)

    return {
        "status": "ok",
        "data": decoded_data
    }

# Update a blog
@blog_root.patch("/update/{_id}")
def UpdateBlog(_id: str, data: UpdateBlogModel):
    request = dict(data)

    return request
    




