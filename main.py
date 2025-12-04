from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.room_router import build_room_router
from application.room_service import RoomService
from infrastructure.mongo_room_repository import MongoRoomRepository
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI(
    title="DormHub API",
    description="API for DormHub application",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Modify this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize MongoDB Repository
mongo_uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
room_repository = MongoRoomRepository(mongo_uri)

# Initialize Services
room_service = RoomService(room_repository)

# Register Routers
room_router = build_room_router(room_service)
app.include_router(room_router)

@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "Welcome to DormHub API"}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run(app, host=host, port=port)
