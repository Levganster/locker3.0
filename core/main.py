# delete any if you don't need it
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import (
    get_redoc_html,
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)


# import from your apps routers
# e.g. - from core.your_app.views import my_router

from core.user.views import router as user_router
from core.auth.views import router as auth_router
from core.websockets.views import router as web_router
from core.control.views import router as control_router
from core.log.views import router as log_router
from core.websockets.views import router as websockets_router

# import base settings
from core.settings import (
    APP_VERSION,
    APP_TITLE,
    DEBUG,
    DESCRIPTION,
    DOCS_URL,
    REDOC_URL,
    ALLOW_METHODS,
    ALLOW_HEADERS,
    ALLOW_CREDENTIALS,
    ALLOW_ORIGINS,
)


# creating app with base settings
app = FastAPI(
    title=APP_TITLE,
    version=APP_VERSION,
    debug=DEBUG,
    description=DESCRIPTION,
    docs_url=None,
    redoc_url=None,
    
    openapi_url="/url_root/openapi.json",
)

# add middlewares
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOW_ORIGINS,
    allow_credentials=ALLOW_CREDENTIALS,
    allow_methods=ALLOW_METHODS,
    allow_headers=ALLOW_HEADERS,
)


@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js",
        swagger_css_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui.css",
    )


@app.get(app.swagger_ui_oauth2_redirect_url, include_in_schema=False)
async def swagger_ui_redirect():
    return get_swagger_ui_oauth2_redirect_html()


@app.get("/redoc", include_in_schema=False)
async def redoc_html():
    return get_redoc_html(
        openapi_url=app.openapi_url,
        title=app.title + " - ReDoc",
        redoc_js_url="https://unpkg.com/redoc@next/bundles/redoc.standalone.js",
    )


# add routers to app
# list of routers to include in app
# e.g. routers = [my_app_router, users_router, auth_router]
routers = [auth_router, user_router, web_router, control_router, log_router, websockets_router]
for router in routers:
    app.include_router(router)
