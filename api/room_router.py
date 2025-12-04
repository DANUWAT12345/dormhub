from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from application.room_service import RoomService
from domain.room_entity import RoomStatus

router = APIRouter(prefix="/rooms", tags=["Rooms"])


class CreateRoomRequest(BaseModel):
    room_id: str


def build_room_router(service: RoomService):

    @router.post("")
    async def create_room(payload: CreateRoomRequest):
        room = await service.create_room(payload.room_id)
        return {"room_id": room.room_id, "status": room.status.value}

    @router.get("/{room_id}")
    async def get_room(room_id: str):
        room = await service.get_room(room_id)
        return {"room_id": room.room_id, "status": room.status.value}

    @router.patch("/{room_id}/occupy")
    async def occupy(room_id: str):
        room = await service.set_status(room_id, RoomStatus.OCCUPIED)
        return {"room_id": room.room_id, "status": room.status.value}

    @router.patch("/{room_id}/free")
    async def free(room_id: str):
        room = await service.set_status(room_id, RoomStatus.AVAILABLE)
        return {"room_id": room.room_id, "status": room.status.value}

    @router.patch("/{room_id}/disable")
    async def disable(room_id: str):
        room = await service.set_status(room_id, RoomStatus.NOTAVAILABLE)
        return {"room_id": room.room_id, "status": room.status.value}

    @router.get("")
    async def list_rooms(status: Optional[str] = None):
        rooms = await service.list_rooms(status)
        return [{"room_id": r.room_id, "status": r.status.value} for r in rooms]

    return router
