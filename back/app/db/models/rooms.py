from sqlalchemy import Column, Integer, String

from ..base import Base


class Room(Base):
    __tablename__ = 'rooms'
    id = Column(
        Integer, nullable=False,
        primary_key=True, autoincrement=True
    )
    tag = Column(
        String, nullable=False
    )
    owner = Column(
        Integer, nullable=False
    )