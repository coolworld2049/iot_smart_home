import uvicorn

from iot_smart_home.devices.http.controller.settings import controller_settings


def main() -> None:
    uvicorn.run(
        "web.application:get_app",
        workers=controller_settings.workers_count,
        host=controller_settings.host,
        port=controller_settings.port,
        reload=controller_settings.reload,
        log_level=controller_settings.log_level.lower(),
        factory=True,
    )


if __name__ == "__main__":
    main()
