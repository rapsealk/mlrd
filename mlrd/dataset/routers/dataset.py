from fastapi import APIRouter

from mlrd.dataset.service import MinioDatasetService

router = APIRouter()


@router.get("/presign")
async def presign_dataset_url():
    service = MinioDatasetService()
    return service.presign()
