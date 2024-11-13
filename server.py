import socketio
import uvicorn
from fastapi import FastAPI
from socketio import AsyncServer

from src.infra.databases.pgdatabase import Base, engine
from src.infra.websocket.namespace import WebsocketNamespace
from src.web.app.asset_administration_shells import asset_administration_shells_router
from src.web.app.histories import history_router
from src.web.app.permissions import permissions_router
from src.web.app.roles import roles_router
from src.web.app.system import system_router
from src.web.app.users import users_router
from src.web.auth.auth import auth_router
from fastapi.middleware.cors import CORSMiddleware

from src.web.middlewares import CheckTokenMiddleware, CheckRoleMiddleware

websocket_server = AsyncServer(async_mode='asgi', cors_allowed_origins=["http://localhost:5173"], logger=True)
app = FastAPI(
    title="AAS Data API",
    redirect_slashes=False,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(CheckTokenMiddleware)
app.add_middleware(CheckRoleMiddleware)

api_version = '/api/v1'
app.include_router(auth_router, prefix=api_version)
app.include_router(asset_administration_shells_router, prefix=api_version)
app.include_router(history_router, prefix=api_version)
app.include_router(system_router, prefix=api_version)

app.include_router(roles_router, prefix=api_version)
app.include_router(permissions_router, prefix=api_version)
app.include_router(users_router, prefix=api_version)

websocket_server.register_namespace(WebsocketNamespace("/"))
websocket_app = socketio.ASGIApp(websocket_server)
app.mount('/', websocket_app)

async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app.add_event_handler('startup', startup)

if __name__ == '__main__':
    uvicorn.run(
        "server:app",
        host='0.0.0.0',
        port=8000,
        lifespan="on",
        loop='uvloop',
        reload=True
    )