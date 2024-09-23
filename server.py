import uvicorn
import sys
from fastapi import FastAPI

from src.config.app_settings import EnvironmentVariables
from src.utils.settings import get_app_settings_by_mode
from src.web.auth.auth import auth_router

app = FastAPI(
    title="AAS Data API"
)


async def startup():
    env_mode = sys.argv[1] if len(sys.argv) > 1 else "development"
    settings = get_app_settings_by_mode(env_mode)
    EnvironmentVariables(settings)

    print(EnvironmentVariables.vars)


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