from abc import ABC, abstractmethod
from typing import List, Optional
from domain.room_entity import Room, RoomStatus


class RoomRepository(ABC):
    @abstractmethod
    async def create_room(self, room: Room):
        pass

    @abstractmethod
    async def get_room(self, room_id: str) -> Optional[Room]:
        pass

    @abstractmethod
    async def update_status(self, room_id: str, status: RoomStatus):
        pass

    @abstractmethod
    async def list_rooms(self, status: Optional[str] = None) -> List[Room]:
        pass
