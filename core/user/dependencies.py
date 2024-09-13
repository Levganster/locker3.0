"""
FastAPI dependencies for the app user
"""

from core.user.service import UserRepository, UserService 

# TODO: define your dependencies here
def get_user_service():
    return UserService(UserRepository)