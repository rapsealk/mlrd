from datetime import datetime
from typing import Optional

from mlrd.models import MLRDBase, PrimaryKey


class ArtifactBase(MLRDBase):
    pass


class ArtifactCreate(ArtifactBase):
    uid: PrimaryKey
    object_name: str
    etag: str


class ArtifactRead(ArtifactBase):
    id: PrimaryKey
    uid: PrimaryKey
    object_name: str
    etag: str
    created_at: datetime
    last_modified_at: datetime


class ArtifactUpdate(ArtifactBase):
    id: PrimaryKey
    uid: Optional[PrimaryKey] = None
    object_name: Optional[str] = None
    etag: Optional[str] = None


class ArtifactDelete(ArtifactBase):
    id: PrimaryKey
