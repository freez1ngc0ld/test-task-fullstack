import jwt
from datetime import datetime, timezone, timedelta
from src.features.admin.exceptions import InvalidTokenException, TokenExpireException


class TokenManager:
    def __init__(self, secret_key: str) -> None:
        self.__secret_key: str = secret_key
        self.__algorithm: str = 'HS256'

    def generate_new_token(self, sub: str, expires: int) -> str:
        payload = {
            'sub': sub,
            'exp': datetime.now(timezone.utc) + timedelta(seconds=expires),
            'iat': datetime.now(timezone.utc)
        }
        return jwt.encode(payload, self.__secret_key, algorithm=self.__algorithm)
    
    def verify_token(self, token: str) -> str:
        try:
            data = jwt.decode(token, self.__secret_key, algorithms=[self.__algorithm])
            sub = data.get('sub')
            if not sub:
                raise InvalidTokenException()
            return sub
        except jwt.ExpiredSignatureError:
            raise TokenExpireException()
        except jwt.PyJWTError:
            raise InvalidTokenException()
        