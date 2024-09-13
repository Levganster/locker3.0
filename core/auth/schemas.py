"""
auth schemas
"""

from pydantic import BaseModel


# define your schemas here 


class AuthCreateSchema(BaseModel):
    username: str
    password: str