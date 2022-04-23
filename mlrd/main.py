import os

from fastapi import FastAPI

from mlrd.api import router as api_router
from mlrd.config import SQLALCHEMY_DATABASE_URI
from mlrd.database import Database
from mlrd.middlewares import add_database_session_middleware

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def create_app() -> FastAPI:
    app = FastAPI(BASE_DIR=base_dir)

    database = Database(SQLALCHEMY_DATABASE_URI)
    database.initialize()

    app.include_router(api_router)

    app = add_database_session_middleware(app=app, database_engine=database.engine)

    @app.on_event("startup")
    def startup():
        pass

    @app.on_event("shutdown")
    def shutdown():
        pass

    return app


app = create_app()
