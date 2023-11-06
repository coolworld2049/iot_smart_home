import uvicorn

from iot_smart_home.devices.http.settings import settings


def main() -> None:
    uvicorn.run(
        "iot_smart_home.devices.http.controller.web.application:get_app",
        workers=settings.workers_count,
        host=settings.controller_host,
        port=settings.controller_port,
        reload=settings.reload,
        log_level=settings.log_level.lower(),
        factory=True,
    )


if __name__ == "__main__":
    main()
