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


def generate_token(user_id, exp, token_type):
    return jwt.encode({
        'id': user_id,
        'type': token_type,
        'exp': exp
    }, algorithm=ALGORITHM, key=settings.SECRET_KEY)


def create_tokens(user_id):
    access_token = generate_token(
        user_id,
        dt.datetime.utcnow() + dt.timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRES),
        'access',
    )
    refresh_token = generate_token(
        user_id,
        dt.datetime.utcnow() + dt.timedelta(days=settings.REFRESH_TOKEN_EXPIRES),
        'refresh',
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
        # if verify_password(token.get('pwd'), user.pwd):
            # return False
        # TODO: verify pwd hash
        return True
    except Exception:
        return False
