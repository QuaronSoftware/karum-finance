from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# from .middleware import AuthMiddlware
from .routers import setup_routers


def create_app():
    app = FastAPI()

    # Setup routers
    setup_routers(app)

    # Setup middlewares
    # app.add_middleware(AuthMiddlware, protected_prefixes=['/api/v1'])
    app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app

