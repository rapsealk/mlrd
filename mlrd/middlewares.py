import uuid
from contextvars import ContextVar
from typing import Final, Optional

from fastapi import FastAPI
from sqlalchemy.engine import Engine
from sqlalchemy.orm import scoped_session, sessionmaker
from starlette.middleware.base import RequestResponseEndpoint
from starlette.requests import Request

REQUEST_ID_CTX_KEY: Final[str] = "request_id"
_request_id_ctx_var: ContextVar[Optional[str]] = ContextVar(REQUEST_ID_CTX_KEY, default=None)


def _get_request_id() -> Optional[str]:
    return _request_id_ctx_var.get()


def add_database_session_middleware(app: FastAPI, database_engine: Engine) -> FastAPI:
    @app.middleware("http")
    async def _(request: Request, call_next: RequestResponseEndpoint):
        request_id = str(uuid.uuid1())

        # we create a per-request id such that we can ensure that our session is scoped for a particular request.
        # see: https://github.com/tiangolo/fastapi/issues/726
        ctx_token = _request_id_ctx_var.set(request_id)

        try:
            session = scoped_session(sessionmaker(bind=database_engine), scopefunc=_get_request_id)
            request.state.db = session()
            response = await call_next(request)
        except Exception as e:
            raise e from None
        finally:
            request.state.db.close()

        _request_id_ctx_var.reset(ctx_token)

        return response

    return app
