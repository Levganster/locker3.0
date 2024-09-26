"""
user schemas
"""

from pydantic import BaseModel


# define your schemas here 


class UserCreateSchema(BaseModel):
    username: str
    password: str
    group: str

class UserGetSchema(UserCreateSchema):
    is_admin: bool