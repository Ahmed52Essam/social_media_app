from pydantic import BaseModel, ConfigDict


class UserPostIn(BaseModel):
    body: str


class UserPost(UserPostIn):
    model_config = ConfigDict(
        from_attributes=True
    )  # ORM mode "pydantic to be able to handle sql objects"
    id: int
    user_id: int


{"id": 0, "body": "This is my post"}


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
    post: UserPost
    comments: list[Comment]


{
    "post": {id: 0, "body": "This is my post"},
    "comments": {"post_id": 0, "body": "This is my comment", "id": 0},
}
