# DormHub

A FastAPI-based backend server for the DormHub application.

## Features

- FastAPI framework for high-performance REST API
- CORS middleware configured
- Health check endpoint
- Auto-generated API documentation (Swagger UI)

## Prerequisites

- Python 3.8+
- pip

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd dormhub
```

2. Create a virtual environment (optional but recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create environment file:
```bash
cp .env.example .env
```

## Running the Server

The server uses environment variables defined in the `.env` file for configuration (e.g., `HOST`, `PORT`, `MONGODB_URI`).

### Development Mode

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```
Or simply:
```bash
python main.py
```
When running with `python main.py`, the application will automatically load variables from the `.env` file.

### Production Mode

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

## API Documentation

Once the server is running, you can access:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## Endpoints

- `GET /` - Root endpoint, returns welcome message
- `GET /health` - Health check endpoint

## Project Structure

```
dormhub/
├── main.py              # Main FastAPI application
├── requirements.txt     # Python dependencies
├── .env.example        # Environment variables template
├── .env                # Environment variables
├── .gitignore          # Git ignore rules
└── README.md           # This file

## Diagrams

### Class Diagram

```text
+----------------+       +-------------------------+
|   RoomStatus   |       |      RoomRepository     |
|----------------|       |      (Interface)        |
| AVAILABLE      |       |-------------------------|
| OCCUPIED       |   +---| create_room(room)       |
| NOTAVAILABLE   |   |   | get_room(id)            |
+----------------+   |   | update_status(id, stat) |
        ^            |   | list_rooms(status)      |
        |            |   +-------------------------+
        .            |                ^
+----------------+   |                | (implements)
|      Room      |   |   +-------------------------+
|----------------|   |   |   MongoRoomRepository   |
| room_id: str   |...|   |-------------------------|
| status: Enum   |   |   | (Implementation of      |
| updated_at: dt |   |   |  Repository methods)    |
+----------------+   |   +-------------------------+
                     |
                     |
+--------------------------+
|       RoomService        |
|--------------------------|
| repo: RoomRepository     |
|--------------------------|
| create_room(id)          |
| get_room(id)             |
| set_status(id, status)   |
| list_rooms(status)       |
+--------------------------+
```

### Usecase Diagram

```text
                      +-----------------------------+
                      |          DormHub            |
                      |-----------------------------|
                      |                             |
      +-------+       |   ( Create Room )           |
      |       |-------|                             |
      | Admin |       |   ( View Room Details )     |
      |       |-------|                             |
      +-------+       |   ( List Rooms )            |
          |           |                             |
          |-----------|   ( Occupy Room )           |
          |           |                             |
          |-----------|   ( Free Room )             |
          |           |                             |
          `-----------|   ( Disable Room )          |
                      |                             |
                      +-----------------------------+
```

### Sequence Diagram

**Scenario: Occupy Room**

```text
User              API Router          RoomService       RoomRepository         MongoDB
 |                    |                    |                   |                  |
 | PATCH /{id}/occupy |                    |                   |                  |
 |------------------->|                    |                   |                  |
 |                    | set_status(id, OCC)|                   |                  |
 |                    |------------------->|                   |                  |
 |                    |                    |   get_room(id)    |                  |
 |                    |                    |------------------>|                  |
 |                    |                    |                   | find_one({_id})  |
 |                    |                    |                   |----------------->|
 |                    |                    |                   |   Room Document  |
 |                    |                    |   Room Entity     |<-----------------|
 |                    |                    |<------------------|                  |
 |                    |                    |                   |                  |
 |                    |                    | update_status(...) |                  |
 |                    |                    |------------------>|                  |
 |                    |                    |                   | update_one(...)  |
 |                    |                    |                   |----------------->|
 |                    |                    |      Success      |<-----------------|
 |                    |      Updated Room  |<------------------|                  |
 |   JSON Response    |<-------------------|                   |                  |
 |<-------------------|                    |                   |                  |
 |                    |                    |                   |                  |
```

### State Machine Diagram

```text
          +-------------+
          |             |
          v             | Free
   +-------------+      |
   |  AVAILABLE  |<-----+
   +-------------+
     |   ^     |
     |   |     | Disable
Occupy |   | Free  |
     |   |     v
     v   |   +--------------+
   +----------+   |              |
   | OCCUPIED |   | NOTAVAILABLE |
   +----------+   |              |
     |   ^   +--------------+
     |   |          |
     |   |          |
     |   |          |
     +---+          |
    Disable         |
                    v
               (Occupied/Free
                transitions
                handled via
                Available)
```

## Development

To add new endpoints, edit `main.py` or create new router modules in an `app/` directory for better organization.

## License

[Add your license here]
