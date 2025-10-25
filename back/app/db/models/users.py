from sqlalchemy import Column, String, Integer
from werkzeug.security import generate_password_hash, check_password_hash

from ..base import Base
from ...auth import create_access_token


class User(Base):
    __tablename__ = 'users'
    id = Column(
        Integer,
        nullable=False, 
        primary_key=True,
        autoincrement=True
    )
    username = Column(
        String,
        nullable=False
    )
    email = Column(
        String,
        nullable=False
    )
    password = Column(
        String,
        nullable=False
    )

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password) -> bool:
        return check_password_hash(self.password, password)
    
    def create_auth_token(self) -> str:
        return create_access_token({'id': self.id})