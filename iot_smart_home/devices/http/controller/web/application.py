import pathlib

from fastapi import FastAPI
from fastapi.responses import UJSONResponse
from starlette.requests import Request
from starlette.templating import Jinja2Templates

from iot_smart_home.core._logging import configure_logging
from iot_smart_home.devices.http.controller.web.api.router import api_router
from iot_smart_home.devices.http.controller.web.lifetime import (
    register_shutdown_event,
    register_startup_event,
)

templates = Jinja2Templates(
    directory=pathlib.Path(__file__).parent.parent.joinpath("templates")
)


def get_app() -> FastAPI:
    configure_logging()
    app = FastAPI(
        title="controller",
        docs_url="/api/docs",
        redoc_url="/api/redoc",
        openurl="/api/openapi.json",
        default_response_class=UJSONResponse,
    )

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
                "reload_every_ms": 2 * 1000,
            },
        )

    return app
