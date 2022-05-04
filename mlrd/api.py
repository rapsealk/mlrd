from fastapi import APIRouter

from mlrd.auth.routers import router as auth_router
from mlrd.dataset.routers import router as dataset_router

router = APIRouter(prefix="/api")

router.include_router(
    auth_router, prefix="/auth", tags=["auth"]
)
router.include_router(
    dataset_router, prefix="/dataset", tags=["dataset"]
)
