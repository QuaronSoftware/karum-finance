from fastapi import FastAPI, APIRouter
from .main import main_router
from .assets import assets_router
#from .auth import auth_router


def setup_routers(app: FastAPI):
    api_v1_router = APIRouter(prefix='/api/v1')

    # Include routers
    api_v1_router.include_router(main_router)
    api_v1_router.include_router(assets_router)

    #app.include_router(auth_router)
    app.include_router(api_v1_router)
