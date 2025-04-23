from fastapi import FastAPI, Request, Response, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import uuid
from user_routes.routes import router as user_router
from admin_routes.routes import router as admin_router
from database.db import init_db
from database.models import add_user
import sys
import os
from fastapi.staticfiles import StaticFiles
from typing import List

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

init_db()
app = FastAPI()

# Include routers
app.include_router(user_router)
app.include_router(admin_router)

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

# Connection manager to handle WebSocket connections
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str, sender: WebSocket):
        for connection in self.active_connections:
            if connection != sender:  # Exclude the sender
                await connection.send_text(message)

manager = ConnectionManager()

@app.middleware("http")
async def assign_user_id(request: Request, call_next):
    user_id = request.cookies.get("user_id")
    if not user_id:
        user_id = str(uuid.uuid4())  # Generate a unique ID
        add_user(user_id)  # Add the user to the database
        response = await call_next(request)
        response.set_cookie(key="user_id", value=user_id)
        return response
    response = await call_next(request)
    return response

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    user_id = request.cookies.get("user_id")
    return templates.TemplateResponse("index.html", {"request": request, "user_id": user_id})

@app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            print(f"Received message from {user_id}: {data}")
            # Check if the sender is the admin
            if user_id == "admin":
                broadcast_message = f"Admin: {data}"
            elif user_id != "admin":
                broadcast_message = f"Admin: {data}"
            # Broadcast the message to all connected clients
            await manager.broadcast(broadcast_message, sender=websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        print(f"User {user_id} disconnected")