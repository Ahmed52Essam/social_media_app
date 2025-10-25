import logging

from social_media_app.database import database, user_table

logger = logging.getLogger(__name__)


async def get_user(email: str):
    query = user_table.select().where(user_table.c.email == email)
    logger.debug("Fetching user from database", extra={"email": email})
    result = await database.fetch_one(query)
    if result:
        return result
