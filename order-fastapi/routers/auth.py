from fastapi import APIRouter

routers = APIRouter()

@routers.get('/auth/')
async def get_user():
    return {'user': 'Authenticated'}