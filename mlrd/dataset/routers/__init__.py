from fastapi import APIRouter

from .dataset import router as dataset_router

router = APIRouter()

router.include_router(
    dataset_router, prefix="", tags=[""]
)
