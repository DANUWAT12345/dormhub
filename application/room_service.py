from typing import Optional
from fastapi import HTTPException

from domain.room_entity import Room, RoomStatus
from domain.room_repository import RoomRepository


class RoomService:

    def __init__(self, repo: RoomRepository):
        self.repo = repo

    async def create_room(self, room_id: str):
        if await self.repo.get_room(room_id):
            raise HTTPException(400, "Room already exists")

        room = Room(room_id=room_id)
        await self.repo.create_room(room)
        return room

    async def get_room(self, room_id: str):
        room = await self.repo.get_room(room_id)
        if not room:
            raise HTTPException(404, "Room not found")
        return room

    async def set_status(self, room_id: str, status: RoomStatus):
        room = await self.repo.get_room(room_id)
        if not room:
            raise HTTPException(404, "Room not found")

        await self.repo.update_status(room_id, status)
        room.status = status
        return room

    async def list_rooms(self, status: Optional[str]):
        return await self.repo.list_rooms(status=status)
