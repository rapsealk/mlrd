from datetime import datetime
from typing import Optional

from mlrd.models import MLRDBase, PrimaryKey


class DatasetBase(MLRDBase):
    pass


class DatasetCreate(DatasetBase):
    uid: PrimaryKey
    display_name: str
    object_name: str
    etag: str
    is_public: bool


class DatasetRead(DatasetBase):
    id: PrimaryKey
    uid: PrimaryKey
    display_name: str
    object_name: str
    etag: str
    is_public: bool
    created_at: datetime
    last_modified_at: datetime


class DatasetUpdate(DatasetBase):
    id: PrimaryKey
    uid: Optional[PrimaryKey] = None
    display_name: Optional[str] = None
    object_name: Optional[str] = None
    etag: Optional[str] = None
    is_public: Optional[bool] = None


class DatasetDelete(DatasetBase):
    id: PrimaryKey
