from sqlalchemy import Boolean, Column, ForeignKey, Integer, String

from mlrd.database import Base
from mlrd.models import TimeStampMixin


class Dataset(Base, TimeStampMixin):
    id = Column(Integer, primary_key=True)
    uid = Column(ForeignKey("user.id"))
    display_name = Column(String(64))
    object_name = Column(String(64), nullable=False)
    etag = Column(String(64), nullable=False)
    is_public = Column(Boolean, default=False, nullable=False)
