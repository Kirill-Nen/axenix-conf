from sqlalchemy.sql import Executable
from sqlalchemy import Result

from ..session import create_session


def executeQuery(query: Executable) -> Result | None:
    session = create_session()
    result = session.execute(query).scalars()
    session.commit()
    return result
    

def executeAddQuery(obj: object) -> None:
    session = create_session()
    session.add(obj)
    session.commit()