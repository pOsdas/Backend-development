from datetime import timedelta

from auth import utils as auth_utils
from core.config import settings
from users.schemas import UserSchema


TOKEN_TYPE_FIELD = "type"
ACCESS_TOKEN_TYPE = "access"
REFRESH_TOKEN_TYPE = "refresh"


def create_jwt(
        token_type: str,
        token_data: dict,
        expires_in: int = settings.auth_jwt.access_token_expires_in,
        expire_timedelta: timedelta | None = None,
) -> str:
    jwt_payload = {TOKEN_TYPE_FIELD: token_type}
    jwt_payload.update(token_data)
    return auth_utils.encode_jwt(
        payload=jwt_payload,
        expires_in=expires_in,
        expire_timedelta=expire_timedelta,
    )


def create_access_token(user: UserSchema) -> str:
    jwt_payload = {
        # subject
        "sub": user.username,
        "username": user.username,
        "email": user.email,
    }

    return create_jwt(
        token_type=ACCESS_TOKEN_TYPE,
        token_data=jwt_payload,
        expires_in=settings.auth_jwt.access_token_expires_in,
    )


def create_refresh_token(user: UserSchema) -> str:
    jwt_payload = {
        "sub": user.username,
        "username": user.username,
    }
    return create_jwt(
        token_type=REFRESH_TOKEN_TYPE,
        token_data=jwt_payload,
        expire_timedelta=timedelta(days=settings.auth_jwt.refresh_token_expire_days),
    )
