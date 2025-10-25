from pydantic import BaseModel

# 1- Create Data model (input / ouput)


class User(BaseModel):
    id: int | None = None
    email: str


class UserIn(User):
    password: str
