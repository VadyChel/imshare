from sqlalchemy import Column, BIGINT, DateTime, String, Integer
from imshare.database import Base


class ApiKey(Base):
    __tablename__ = "api_keys"

    id = Column(BIGINT, autoincrement=True, primary_key=True)
    time = Column(DateTime(timezone=True))
    api_key = Column(String(64))
    max_file_length = Column(Integer, nullable=False)


class File(Base):
    __tablename__ = "files"

    id = Column(BIGINT, autoincrement=True, primary_key=True)
    filename = Column(String(45))
    name = Column(String(45))
    uploaded_by = Column(String(64))