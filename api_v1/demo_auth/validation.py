from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError
from starlette import status

from api_v1.demo_auth.crud import users_db
from api_v1.demo_auth.helpers import TOKEN_TYPE_FIELD, ACCESS_TOKEN_TYPE, REFRESH_TOKEN_TYPE
from auth import utils as auth_utils
from users.schemas import UserSchema

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="api/v1/demo_auth/jwt/login/",
)


def get_current_token_payload(
    # credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
    token: str = Depends(oauth2_scheme)
) -> UserSchema:
    # token = credentials.credentials
    try:
        payload = auth_utils.decode_jwt(
            token=token
        )
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token error"
        )
    return payload


def validate_token_type(
        payload: dict,
        token_type: str
) -> bool:
    current_token_type = payload.get(TOKEN_TYPE_FIELD)
    if current_token_type == token_type:
        return True
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"Invalid token type {current_token_type!r} expected {token_type!r}",
    )


def get_user_by_token_sub(payload: dict) -> UserSchema:
    username: str | None = payload.get("sub")
    if user := users_db.get(username):
        return user
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token invalid or expired"
    )


def get_auth_user_from_token_of_type(token_type: str):
    def get_auth_user_from_token(
            payload: dict = Depends(get_current_token_payload),
    ) -> UserSchema:
        validate_token_type(payload=payload, token_type=token_type)
        return get_user_by_token_sub(payload)
    return get_auth_user_from_token


get_current_auth_user = get_auth_user_from_token_of_type(ACCESS_TOKEN_TYPE)
get_current_auth_user_for_refresh = get_auth_user_from_token_of_type(REFRESH_TOKEN_TYPE)
