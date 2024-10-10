from fastapi import APIRouter

history_router = APIRouter(
    prefix="/histories",
    tags=["History Data"]
)

@history_router.get('/')
async def get_historized_data():
    ...