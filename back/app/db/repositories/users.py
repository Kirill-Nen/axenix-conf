from sqlalchemy import select, insert, update, delete, or_
from werkzeug.security import generate_password_hash
from typing import Union

from .queries import executeQuery, executeAddQuery
from ..models.users import User


class UserRepository:
    @staticmethod
    def add(
        username: str,
        password: str,
        email: str
    ) -> User:
        user = User(
            username=username,
            password=generate_password_hash(password),
            email=email
        )
        executeAddQuery(user)
        return user
    
    @staticmethod
    def validate_exists(
        username: str,
        email: str
    ) -> bool:
        result = executeQuery(
            select(User).where(or_(
                User.username == username,
                User.email == email
            ))
        )
        return True if not result.first() else False
    
    @staticmethod
    def get(*args) -> Union[User, None]:
        result = executeQuery(select(User).where(*args))
        result = result.scalar_one_or_none()
        return result
