# main.py

import os
import uvicorn


def api(
    config: str = os.getenv("CONFIG_FILE", ".env"),
    port: int = 8000,
    workers: int = 1,
    dev: bool = True,
):
    os.environ["CONFIG_FILE"] = config

    uvicorn.run(
        "api.app:init",  
        host="0.0.0.0",
        port=port,
        workers=workers,
        reload=dev,
        access_log=dev,
        factory=True
    )


if __name__ == "__main__":
    api()
