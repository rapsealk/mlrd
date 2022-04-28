from enum import Enum

from sqlalchemy import Column, ForeignKey, Integer, String

from mlrd.database import Base
from mlrd.models import TimeStampMixin


class Session(Base, TimeStampMixin):
    id = Column(Integer, primary_key=True)
    uid = Column(ForeignKey("user.id"), nullable=False)
    artifact_id = Column(ForeignKey("artifact.id"), nullable=False)
    dataset_id = Column(ForeignKey("dataset.id"), nullable=False)
    device_id = Column(ForeignKey("device.id"), nullable=False)
    container = Column(String(64), nullable=False)
    state = Column(String(9), nullable=False)

    class State(Enum):
        QUEUED = "QUEUED"
        ALLOCATED = "ALLOCATED"
        RUNNING = "RUNNING"
        PAUSED = "PAUSED"
        EXITED = "EXITED"
