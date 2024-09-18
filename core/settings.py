"""
App info, which includes in FastAPI object
e.g - app = FastAPI(title='my_app', version='0.1') e.t.c
"""

APP_VERSION = '0.1'
APP_TITLE = 'FastAPI app'
DESCRIPTION = 'Your desc'

# WARNING: change this to False on release
DEBUG = True

# url for openapi interactive docs
DOCS_URL = "/docs"
REDOC_URL = "/redoc"

# CORS settings
ALLOW_ORIGINS = ["*"]
ALLOW_METHODS = ["*"]
ALLOW_HEADERS = ["*"]
ALLOW_CREDENTIALS = True


# Database settings
ASYNC_DATABASE_URL = "postgresql+asyncpg://gen_user:r|^qu&n>Z.72oQ@192.168.0.6:5432/default_db"
SYNC_DATABASE_URL = "postgresql://gen_user:r|^qu&n>Z.72oQ@192.168.0.6:5432/default_db" # for alembic migrations

