
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class LoginRequest(BaseModel):
    username: str = Field(..., description="Enter your account username")
    password: str = Field(..., description="Enter your account password")

class RoomsAvailableRequest(BaseModel):
    access_token: str = Field(..., description="Enter your access token")
    room_booking_slot_datetime: str = Field(..., description="Enter your desired booking slot datetime in 'YYYY-MM-DD HH:MM' format")
