from argon2 import PasswordHasher
from hashlib import md5
from config import settings
from datetime import datetime, timedelta, timezone
import jwt

ALGORITHM = 'HS256'
ph = PasswordHasher()


def get_password_hash(password) -> str:
    return ph.hash(password)


def verify_password(pwd, hashed_pwd) -> bool:
    return ph.verify(hashed_pwd, pwd)


def generate_token(user_id: int, exp: datetime,
                   token_type: str, hashed_password: str) -> str:
    return jwt.encode({
        'id': user_id,
        'type': token_type,
        'exp': exp,
        'sign': md5(hashed_password.encode()).hexdigest()
    }, algorithm=ALGORITHM, key=settings.SECRET_KEY)


def create_tokens(user_id: int, hashed_password: str) -> dict:
    access_token = generate_token(
        user_id,
        datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRES),
        'access',
        hashed_password
    )
    refresh_token = generate_token(
        user_id,
        datetime.now(timezone.utc) + timedelta(
            days=settings.REFRESH_TOKEN_EXPIRES),
        'refresh',
        hashed_password
    )

    return {
        'access_token': access_token,
        'refresh_token': refresh_token
    }


def decode_token(token: str) -> dict:
    return jwt.decode(
        token, algorithms=[ALGORITHM],
        key=settings.SECRET_KEY
    )


def is_valid_token(token: str, password: str) -> bool:
    try:
        token = decode_token(token)
        return token.get('sign') == md5(password.encode()).hexdigest()
    except Exception:
        return False
