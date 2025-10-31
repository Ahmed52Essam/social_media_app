import logging

from fastapi import APIRouter, HTTPException, Request

from social_media_app.database import comment_table, database, post_table
from social_media_app.models.post import (
    Comment,
    CommentIn,
    UserPost,
    UserPostIn,
    UserPostWithComments,
)
from social_media_app.models.user import User
from social_media_app.security import get_current_user, oauth2scheme

router = APIRouter()

logger = logging.getLogger(__name__)


async def find_post(post_id: int):
    logger.info(f"Finding post with ID:{post_id}")
    query = post_table.select().where(post_table.c.id == post_id)
    logger.debug(query)
    return await database.fetch_one(query)


@router.post("/post", response_model=UserPost, status_code=201)
async def create_post(post: UserPostIn, request: Request):
    logger.info(f"Creating post: {post}")
    current_user: User = await get_current_user(await oauth2scheme(request=request))  # noqa

    data = post.model_dump()
    query = post_table.insert().values(data)
    logger.debug(query)
    last_record_id = await database.execute(query)
    return {**data, "id": last_record_id}


@router.get("/post", response_model=list[UserPost])
async def get_all_posts():
    logger.info("Featching all posts")
    query = post_table.select()
    logger.debug(query)
    return await database.fetch_all(query)


@router.get("/post/{post_id}/comments", response_model=list[Comment])
async def get_comments_on_post(post_id: int):
    logger.info(f"Fetching comments for post ID: {post_id}")
    query = comment_table.select().where(comment_table.c.post_id == post_id)
    logger.debug(query)
    return await database.fetch_all(query)


@router.get("/post/{post_id}", response_model=UserPostWithComments)
async def get_post_with_comments(post_id: int):
    logger.info(f"Fetching post with comments for post ID: {post_id}")
    post = await find_post(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    return {"post": post, "comments": await get_comments_on_post(post_id)}


@router.post("/comment", response_model=Comment, status_code=201)
async def create_comment(comment: CommentIn, request: Request):
    logger.info(f"creating comment: {comment}")
    current_user: User = await get_current_user(await oauth2scheme(request=request))  # noqa

    post = await find_post(comment.post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    data = comment.model_dump()
    query = comment_table.insert().values(data)
    last_record_id = await database.execute(query)
    logger.debug(query)
    return {**data, "id": last_record_id}
