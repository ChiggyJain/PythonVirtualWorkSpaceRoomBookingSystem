
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any, Literal


class LoginRequest(BaseModel):
    username: str = Field(..., description="Enter your account username")
    password: str = Field(..., description="Enter your account password")

class TeamsListRequest(BaseModel):
    access_token: str = Field(..., description="Enter your logged-in account access token")
    

class RoomsAvailableRequest(BaseModel):
    access_token: str = Field(..., description="Enter your logged-in account access token")
    room_type: Literal['Private', 'Conference', 'Shared-Desk'] = Field(..., description="Enter your desired room type: Private, Conference, or Shared-Desk")
    room_booking_slot_datetime: str = Field(..., description="Enter your desired booking slot datetime in 'YYYY-MM-DD HH:MM' format")

class CancelBookedRoomRequest(BaseModel):
    access_token: str = Field(..., description="Enter your logged-in account access token")
    room_booking_id: str = Field(..., description="Enter your booked room booking id to cancel the booking")

class RoomBookingRequest(BaseModel):
    access_token: str = Field(..., description="Enter your logged-in account access token")
    team_id: int = Field(None, description="If you are booking room for TEAM then please provide team_id ELSE 0")
    room_id: int = Field(..., description="Enter room id")
    room_booking_slot_datetime: str = Field(..., description="Enter your desired booking slot datetime in 'YYYY-MM-DD HH:MM' format")
