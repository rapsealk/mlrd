from fastapi import APIRouter

from mlrd.auth.views import router as auth_router

router = APIRouter(prefix="/api")

router.include_router(
    auth_router, prefix="/auth", tags=["auth"]
)
