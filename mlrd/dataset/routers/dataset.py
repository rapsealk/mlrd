from fastapi import APIRouter

from mlrd.dataset.service import DatasetService, MinioStorageService

router = APIRouter()


@router.get("/")
async def get_datasets():
    pass


@router.get("/presign")
async def presign_dataset_url():
    service = DatasetService(storage=MinioStorageService())
    return service.presign()


@router.post("/")
async def add_dataset():
    pass


@router.delete("/")
async def delete_dataset():
    pass
