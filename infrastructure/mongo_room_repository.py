from datetime import datetime, timezone
from motor.motor_asyncio import AsyncIOMotorClient
from typing import List, Optional

from domain.room_repository import RoomRepository
from domain.room_entity import Room, RoomStatus


class MongoRoomRepository(RoomRepository):

    def __init__(self, uri: str):
        client = AsyncIOMotorClient(uri)
        db = client["dormhub"]
        self.collection = db["rooms"]

    async def create_room(self, room: Room):
        await self.collection.insert_one({
            "_id": room.room_id,
            "status": room.status.value,  # enum to string
            "updated_at": room.updated_at,
        })

    async def get_room(self, room_id: str) -> Optional[Room]:
        doc = await self.collection.find_one({"_id": room_id})
        if not doc:
            return None

        return Room(
            room_id=doc["_id"],
            status=RoomStatus(doc["status"]),  # convert string to enum
            updated_at=doc["updated_at"],
        )

    async def update_status(self, room_id: str, status: RoomStatus):
        await self.collection.update_one(
            {"_id": room_id},
            {
                "$set": {
                    "status": status.value,
                    "updated_at": datetime.now(timezone.utc),
                }
            }
        )

    async def list_rooms(self, status: Optional[str] = None) -> List[Room]:
        query = {}
        if status:
            query["status"] = status.upper()

        cursor = self.collection.find(query)
        rooms = []

        async for doc in cursor:
            rooms.append(
                Room(
                    room_id=doc["_id"],
                    status=RoomStatus(doc["status"]),
                    updated_at=doc["updated_at"]
                )
            )
        return rooms
