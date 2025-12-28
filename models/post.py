from typing import Optional
from pydantic import BaseModel, ConfigDict


class UserPostIn(BaseModel):
    body: str


class UserPost(UserPostIn):
    model_config = ConfigDict(
        from_attributes=True
    )  # ORM mode "pydantic to be able to handle sql objects"
    id: int
    user_id: int
    image_url: Optional[str] = None


{"id": 0, "body": "This is my post"}


class UserPostwithLikes(UserPost):
    likes: int
    model_config = ConfigDict(
        from_attributes=True
    )  # ORM mode "pydantic to be able to handle sql objects"


class CommentIn(BaseModel):
    body: str
    post_id: int


class Comment(CommentIn):
    model_config = ConfigDict(
        from_attributes=True
    )  # ORM mode "pydantic to be able to handle sql objects"
    id: int
    user_id: int


{"id": 0, "body": "This is my comment", "post_id": 0}


class UserPostWithComments(BaseModel):
    post: UserPostwithLikes
    comments: list[Comment]


{
    "post": {id: 0, "body": "This is my post"},
    "comments": {"post_id": 0, "body": "This is my comment", "id": 0},
}


class PostLikeIn(BaseModel):
    post_id: int


class PostLike(PostLikeIn):
    id: int
    user_id: int
