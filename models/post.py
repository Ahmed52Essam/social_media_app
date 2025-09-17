from pydantic import BaseModel


class UserPostIn(BaseModel):
    body: str


class UserPost(UserPostIn):
    id: int


{"id": 0, "body": "This is my post"}


class CommentIn(BaseModel):
    body: str
    post_id: int


class Comment(CommentIn):
    comment_id: int


{"comment_id": 0, "body": "This is my comment", "post_id": 0}


class UserPostWithComments(BaseModel):
    post: UserPost
    comments: list[Comment]


{
    "post": {id: 0, "body": "This is my post"},
    "comments": {"post_id": 0, "body": "This is my comment", "comment_id": 0},
}
