from sqlalchemy import Column, BIGINT, DATETIME, String
from imshare.database import Base


class ApiKey(Base):
    __tablename__ = "api_keys"

    id = Column(BIGINT, primary_key=True)
    time = Column(DATETIME)
    api_key = Column(String(64))


class Image(Base):
    __tablename__ = "images"

    id = Column(BIGINT, primary_key=True)
    filename = Column(String(45))
    name = Column(String(45))
    uploaded_by = Column(String(64))