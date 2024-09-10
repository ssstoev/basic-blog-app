# in this file we are gonna wrap all the endpoints

from fastapi import APIRouter

entry_root = APIRouter()

#create an endpoint
# the forard slash is the main route
@entry_root.get("/")
def api_runner():
    response =  {
        'status': 'ok',
        'message': 'API is running'
    }

    return response