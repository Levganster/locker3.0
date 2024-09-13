"""
user schemas
"""

from pydantic import BaseModel


# define your schemas here 


class UserCreateSchema(BaseModel):
    username: str
    password: str

class UserGetSchema(UserCreateSchema):
    is_admin: bool = False