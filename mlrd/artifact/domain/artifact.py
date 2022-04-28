from sqlalchemy import Column, ForeignKey, Integer, String

from mlrd.database import Base
from mlrd.models import TimeStampMixin


class Artifact(Base, TimeStampMixin):
    id = Column(Integer, primary_key=True)
    uid = Column(ForeignKey("user.id"))
    object_name = Column(String(64), nullable=False)
    etag = Column(String(64), nullable=False)
