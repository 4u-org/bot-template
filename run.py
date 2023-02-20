import uvicorn
import config as cnf

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=cnf.WEB_SERVER_HOST,
        port=cnf.WEB_SERVER_PORT,
        reload=cnf.LOCAL
    )