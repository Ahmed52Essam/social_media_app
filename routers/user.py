import logging

from fastapi import APIRouter, HTTPException, status

from social_media_app.database import database, user_table
from social_media_app.models.user import UserIn
from social_media_app.security import get_user

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/register", status_code=201)
async def register(user: UserIn):
    if await get_user(user.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with that email already exists!",
        )
    # This is a very Bad Idea! you should never store passwords in plain text!
    query = user_table.insert().values(email=user.email, password=user.password)
    logger.debug(query)
    await database.execute(query)
    return {"detail": "User created"}
