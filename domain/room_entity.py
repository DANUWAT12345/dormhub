from datetime import datetime, timezone
from enum import Enum


class RoomStatus(str, Enum):
    AVAILABLE = "AVAILABLE"
    OCCUPIED = "OCCUPIED"
    NOTAVAILABLE = "NOTAVAILABLE"


class Room:
    def __init__(
        self,
        room_id: str,
        status: RoomStatus = RoomStatus.AVAILABLE,
        updated_at=None
    ):
        self.room_id = room_id
        self.status = status

        # Always keep UTC+0 explicitly
        self.updated_at = updated_at or datetime.now(timezone.utc)
