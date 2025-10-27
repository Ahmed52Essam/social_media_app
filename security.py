import logging

from passlib.context import CryptContext

from social_media_app.database import database, user_table

logger = logging.getLogger(__name__)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hashed(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


async def get_user(email: str):
    query = user_table.select().where(user_table.c.email == email)
    logger.debug("Fetching user from database", extra={"email": email})
    result = await database.fetch_one(query)
    if result:
        return result
