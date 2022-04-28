from sqlalchemy import Column, Integer, String

from mlrd.database import Base
from mlrd.models import TimeStampMixin


class Device(Base, TimeStampMixin):
    id = Column(Integer, primary_key=True)
    address = Column(String(15), nullable=False)
    uuid = Column(String(32), unique=True)
    total_global_memory = Column(Integer, nullable=False)
