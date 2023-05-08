import uvicorn

from imshare.config import config

if __name__ == "__main__":
    uvicorn.run(
        "imshare.api.main:app",
        port=config.app.port,
        host=config.app.host,
        reload=config.app.reload,
        proxy_headers=config.app.proxy_headers,
        use_colors=True,
        log_config="imshare/config/logging.json"
    )