import jwt
import os
import datetime

SECRET_KEY = 'software1234567'
ALGORITHM = 'HS256'

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    to_encode['exp'] = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=365)
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.exceptions.InvalidSignatureError:
        print('err: неверная подпись токена.')
    except jwt.exceptions.ExpiredSignatureError:
        print('err: срок действия токена истек.')
    except jwt.exceptions.InvalidTokenError:
        print('err: неверный токен.')
    except Exception as e:
        print(f'err: произошла непредвиденная ошибка: {e}')