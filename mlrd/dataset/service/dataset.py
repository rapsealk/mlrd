from abc import ABC
from datetime import timedelta
from typing import Optional
from uuid import uuid4

import minio

from mlrd.config import MINIO_ACCESS_KEY, MINIO_BUCKET_NAME, MINIO_ENDPOINT, MINIO_SECRET_KEY


class BaseDatasetService(ABC):
    def __init__(self):
        pass

    def presign(self):
        raise NotImplementedError()


class MinioDatasetService(BaseDatasetService):
    def __init__(self):
        super(MinioDatasetService, self).__init__()

    def presign(
        self,
        bucket_name: str = MINIO_BUCKET_NAME,
        object_name: Optional[str] = None,
        expires: timedelta = timedelta(minutes=3)
    ) -> Optional[str]:
        object_name = object_name or str(uuid4())
        client = minio.Minio(
            endpoint=MINIO_ENDPOINT,
            access_key=MINIO_ACCESS_KEY,
            secret_key=MINIO_SECRET_KEY,
            secure=False
        )
        if not client.bucket_exists(bucket_name):
            client.make_bucket(bucket_name)
        try:
            url = client.presigned_put_object(bucket_name, object_name, expires=expires)
        except ValueError:
            return None
        return url
