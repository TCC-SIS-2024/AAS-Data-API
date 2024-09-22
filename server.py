import uvicorn

from fastapi import FastAPI

app = FastAPI(
    title="AAS Data API"
)


if __name__ == '__main__':
    uvicorn.run(
        "server:app",
        host='0.0.0.0',
        port=8000,
        loop='uvloop',
        reload=True
    )