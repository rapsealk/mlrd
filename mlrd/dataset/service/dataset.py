from datetime import timedelta

import minio


def get_presigned_url(bucket_name: str, object_name: str, expires: timedelta = timedelta(minutes=3)) -> str:
    client = minio.Minio(
        endpoint="localhost:9000",
        access_key="root",
        secret_key="00000000",
        secure=False
    )
    url = client.presigned_put_object(bucket_name, object_name, expires=expires)
    return url
