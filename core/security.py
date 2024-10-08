from passlib.context import CryptContext
from config import settings
import datetime as dt
import jwt

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
ALGORITHM = 'HS256'


def get_password_hash(password):
    return pwd_context.hash(password)


def verify_password(pwd, hashed_pwd):
    return pwd_context.verify(pwd, hashed_pwd)


def generate_token(user_id, exp, token_type, hashed_password):
    return jwt.encode({
        'id': user_id,
        'type': token_type,
        'exp': exp,
        'hashed_password': hashed_password
    }, algorithm=ALGORITHM, key=settings.SECRET_KEY)


def create_tokens(user_id, hashed_password):
    access_token = generate_token(
        user_id,
        dt.datetime.utcnow() + dt.timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRES),
        'access',
        hashed_password
    )
    refresh_token = generate_token(
        user_id,
        dt.datetime.utcnow() + dt.timedelta(days=settings.REFRESH_TOKEN_EXPIRES),
        'refresh',
        hashed_password
    )

    return {
        'access_token': access_token,
        'refresh_token': refresh_token
    }


def decode_token(token):
    return jwt.decode(
        token, algorithms=[ALGORITHM],
        key=settings.SECRET_KEY
    )


def is_valid_token(token, user):
    try:
        token = decode_token(token)
        if token.get('hashed_password') != user.password:
            return False
        return True
    except Exception:
        return False
