from importlib import metadata

from fastapi import FastAPI
from fastapi.responses import UJSONResponse
from starlette.requests import Request
from starlette.templating import Jinja2Templates

from iot_smart_home.devices.http.controller.web.api.router import api_router
from iot_smart_home.devices.http.controller.web.lifetime import (
    register_shutdown_event,
    register_startup_event,
)
from iot_smart_home.core._logging import configure_logging


def get_app() -> FastAPI:
    configure_logging()
    app = FastAPI(
        title="controller",
        version=metadata.version("controller"),
        docs_url="/api/docs",
        redoc_url="/api/redoc",
        openapi_url="/api/openapi.json",
        default_response_class=UJSONResponse,
    )
    templates = Jinja2Templates(directory="templates")

    register_startup_event(app)
    register_shutdown_event(app)

    app.include_router(router=api_router, prefix="/api")

    @app.get("/")
    def index(request: Request):
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "devices": request.app.state.devices,
                "reload_every_ms": 4 * 1000,
            },
        )

    return app
