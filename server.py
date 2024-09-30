import uvicorn
from fastapi import FastAPI
from src.infra.databases.pgdatabase import Base, engine
from src.web.auth.auth import auth_router

app = FastAPI(
    title="AAS Data API"
)


async def startup():

    # async with engine.begin() as conn:
    #     await conn.run_sync(Base.metadata.drop_all)
    #     await conn.run_sync(Base.metadata.create_all)
    #
    # await engine.dispose()
    ...

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