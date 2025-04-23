from fastapi import APIRouter, Request
from database.models import save_message

router = APIRouter()

@router.post("/send_message")
async def send_message(request: Request):
    data = await request.json()
    user_id = request.cookies.get("user_id")
    print(f"User ID: {user_id}, Message: {data.get('message')}")  # Debug log
    if not user_id or not data.get("message"):
        return {"error": "Invalid data"}
    save_message(user_id, data.get("message"), is_admin=False)  # Save the user's message
    return {"status": "success"}