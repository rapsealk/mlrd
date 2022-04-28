from datetime import datetime
from typing import Optional

from mlrd.models import MLRDBase, PrimaryKey


class SessionBase(MLRDBase):
    pass


class SessionCreate(SessionBase):
    uid: PrimaryKey
    artifact_id: PrimaryKey
    dataset_id: PrimaryKey
    device_id: PrimaryKey


class SessionRead(SessionBase):
    id: PrimaryKey
    uid: PrimaryKey
    artifact_id: PrimaryKey
    dataset_id: PrimaryKey
    device_id: PrimaryKey
    container: Optional[str] = None
    state: str
    created_at: datetime
    last_modified_at: datetime


class SessionUpdate(SessionBase):
    id: PrimaryKey
    uid: Optional[PrimaryKey] = None
    artifact_id: Optional[PrimaryKey] = None
    dataset_id: Optional[PrimaryKey] = None
    device_id: Optional[PrimaryKey] = None
    container: Optional[str] = None
    state: Optional[str] = None


class SessionDelete(SessionBase):
    id: PrimaryKey
