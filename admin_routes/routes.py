from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from database.models import get_all_users, get_user_messages, save_message
from pydantic import BaseModel

templates = Jinja2Templates(directory="templates")
router = APIRouter()

class MessageRequest(BaseModel):
    user_id: str
    message: str

@router.get("/admin", response_class=HTMLResponse)
async def admin_page(request: Request):
    users = get_all_users()  # Fetch all users from the database
    return templates.TemplateResponse("admin.html", {"request": request, "users": users})

@router.get("/admin/messages/{user_id}")
async def get_messages(user_id: str):
    messages = get_user_messages(user_id)
    print(f"Fetching messages for User ID: {user_id}, Messages: {messages}")  # Debug log
    return {"messages": [dict(msg) for msg in messages]}  # Convert sqlite3.Row to dict

@router.post("/admin/send_message")
async def admin_send_message(request: MessageRequest):
    print(f"Admin is sending a message to User ID: {request.user_id}, Message: {request.message}")  # Debug log
    save_message(request.user_id, request.message, is_admin=True)  # Save the admin's message
    return {"status": "success"}

@router.get("/admin/chat/{user_id}", response_class=HTMLResponse)
async def admin_chat(request: Request, user_id: str):
    return templates.TemplateResponse("chat.html", {"request": request, "user_id": user_id})

@router.post("/send_message")
async def send_message(request: Request):
    data = await request.json()
    user_id = request.cookies.get("user_id")
    message = data.get("message")
    save_message(user_id, message, is_admin=False)
    return {"status": "success"}

@router.get("/messages")
async def get_user_messages_route(request: Request):
    user_id = request.cookies.get("user_id")
    messages = get_user_messages(user_id)
    print(f"Fetching messages for User ID: {user_id}, Messages: {messages}")  # Debug log
    return {"messages": [dict(msg) for msg in messages]}



