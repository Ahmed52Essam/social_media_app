import pytest
from jose import jwt

from social_media_app import security


@pytest.mark.anyio
async def test_access_token_expire_minutes():
    assert security.access_token_expire_minutes() == 30


@pytest.mark.anyio
async def test_confirmation_token_expire_minutes():
    assert security.confirmation_token_expire_minutes() == 1440


@pytest.mark.anyio
async def test_create_access_token():
    token = "email@test.net"
    token = security.create_access_token(token)
    assert {"sub": "email@test.net", "type": "access"}.items() <= jwt.decode(
        token, key=security.SECRET_KEY, algorithms=[security.ALGORITHM]
    ).items()


@pytest.mark.anyio
async def test_create_confirmation_token():
    token = "email@test.net"
    token = security.create_confirmation_token(token)
    assert {"sub": "email@test.net", "type": "confirmation"}.items() <= jwt.decode(
        token, key=security.SECRET_KEY, algorithms=[security.ALGORITHM]
    ).items()


@pytest.mark.anyio
async def test_password_hashes():
    password = "password"
    assert security.verify_password(password, security.get_password_hashed(password))


# 4- Create test for get user function


@pytest.mark.anyio
async def test_get_user(registered_user: dict):
    user = await security.get_user(registered_user["email"])
    assert user.email == registered_user["email"]


@pytest.mark.anyio
async def test_get_user_not_found():
    user = await security.get_user("test@example.com")
    assert user is None


@pytest.mark.anyio
async def test_authenticate_user_exist(registered_user: dict):
    user = await security.authenticate_user(
        registered_user["email"], registered_user["password"]
    )
    assert user.email == registered_user["email"]


@pytest.mark.anyio
async def test_authenticate_user_not_exist():
    with pytest.raises(security.HTTPException):
        await security.authenticate_user("anyemail", "1234")


@pytest.mark.anyio
async def test_authenticate_user_exist_wrong_password(registered_user: dict):
    with pytest.raises(security.HTTPException):
        await security.authenticate_user(registered_user["email"], "wrong password")


@pytest.mark.anyio
async def test_get_current_user(registered_user: dict):
    token = security.create_access_token(registered_user["email"])
    user = await security.get_current_user(token)
    assert user.email == registered_user["email"]


@pytest.mark.anyio
async def test_get_current_user_invalid_token():
    with pytest.raises(security.HTTPException):
        await security.get_current_user("Invalid token")


@pytest.mark.anyio
async def test_get_current_user_wrong_type_token(registered_user: dict):
    token = security.create_confirmation_token(registered_user["email"])
    with pytest.raises(security.HTTPException):
        await security.get_current_user(token)
