import uvicorn
import config

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=config.WEB_SERVER_HOST,
        port=config.WEB_SERVER_PORT,
        reload=config.LOCAL
    )