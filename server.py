import uvicorn

from fastapi import FastAPI

from src.utils.events import startup
from src.web.auth.auth import auth_router

app = FastAPI(
    title="AAS Data API"
)

app.include_router(auth_router)
app.add_event_handler('startup', startup)




if __name__ == '__main__':
    uvicorn.run(
        "server:app",
        host='0.0.0.0',
        port=8000,
        loop='uvloop',
        reload=True
    )