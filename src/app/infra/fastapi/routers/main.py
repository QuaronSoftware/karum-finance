from fastapi import APIRouter


main_router = APIRouter()


@main_router.get('/health')
async def ok():
    return {'ok': True}

