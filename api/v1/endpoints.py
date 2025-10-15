

from fastapi import APIRouter, Form, HTTPException 
from datetime import datetime
from datetime import time as dt_time  # rename to avoid clash
from fastapi.responses import JSONResponse
from api.v1.schemas import *
from api.v1.login_queries import *
from api.v1.room_booking_system_queries import *
from utils.utils import *

router = APIRouter()






# login api
@router.post("/login/", summary="User Login Authentication")
async def login_user(loginRequestFormData: LoginRequest):

    """
        This api is used for authenticate user login details. 
        If login success then return access-token details with validity of 15minutes only.
        If login failed then return error messages.
        - **username**: Enter your account username 
        - **password**: Enter your account password
    """

    rspDataObj = {
        "status_code": 401,
        "messages": [],
        "data": {}
    }

    try:
        authenticatedUsrLoginDetails = await getLoginUserDetails(loginRequestFormData.username, loginRequestFormData.password)
        print(f"authenticatedUsrLoginDetails: {authenticatedUsrLoginDetails}")
        if authenticatedUsrLoginDetails:
            access_token, access_token_expire_time = createLoginUserAccessToken(data={"userId": authenticatedUsrLoginDetails['userId']})       
            rspDataObj['status_code'] = 200
            rspDataObj['messages'] = ["User login successfully."]
            rspDataObj['data'] = {
                "token_type": "bearer",
                "access_token": access_token,
                "access_token_expire_time": str(access_token_expire_time)
            }
        else:
            rspDataObj['status_code'] = 401
            rspDataObj['messages'] = ["Invalid username or password."]
    except Exception as e:
        print(f"Exception error occured: {e}")
        rspDataObj['status_code'] = 500
        rspDataObj['messages'] = [f"Error occured: {str(e)}"]

    #return rspDataObj
    return JSONResponse(status_code=rspDataObj['status_code'], content=rspDataObj)




# rooms-available api
@router.get("/rooms/available", summary="Rooms Available for Booking")
async def rooms_available(access_token: str, room_type:str, room_booking_slot_datetime: str):

    """
        This api is used for check available rooms for booking on given date-time slot.
        - **access_token**: Enter your access token
        - **room_booking_slot_datetime**: Enter your desired booking slot datetime in 'YYYY-MM  DD HH:MM' format  
    """

    rspDataObj = {
        "status_code": 401,
        "messages": [],
        "data": {}
    }

    try:

        # checking room_type
        if room_type not in ['Private', 'Conference', 'Shared-Desks']:
            rspDataObj['status_code'] = 400
            rspDataObj['messages'] = [f"Invalid room-type: {room_type}. Accepted room-types are 'Private', 'Conference', 'Shared-Desk'."]
            return JSONResponse(status_code=rspDataObj['status_code'], content=rspDataObj)

        # checking room_booking_slot_datetime
        if room_booking_slot_datetime:
            # Parse string to datetime object
            slot_dt = datetime.strptime(room_booking_slot_datetime, "%Y-%m-%d %H:%M:%S")
            # Check if time is within allowed working hours
            if not (dt_time(9, 0) <= slot_dt.time() <= dt_time(18, 0)):
                rspDataObj['status_code'] = 400
                rspDataObj['messages'] = ["Slot time must be between 09:00 and 18:00."]
                return JSONResponse(status_code=400, content=rspDataObj)
            
            # Check if minute is zero (hourly slot)
            if slot_dt.minute != 0 or slot_dt.second != 0:
                rspDataObj['status_code'] = 400
                rspDataObj['messages'] = ["Slot must be on the hour, e.g: 10:00, 11:00."]
                return JSONResponse(status_code=400, content=rspDataObj)


        # decoding access-token         
        decodedAccessTokenData = decodeLoginUserAccessToken(access_token)
        print(f"decodedAccessTokenData: {decodedAccessTokenData}")
        if decodedAccessTokenData:
            userId = decodedAccessTokenData["userId"]
            # fetching available rooms details
            availableRoomsDetails = await getAvailableRoomsDetails(room_type, room_booking_slot_datetime)
            print(f"availableRoomsDetails: {availableRoomsDetails}")
            if availableRoomsDetails:
                rspDataObj['status_code'] = 200
                rspDataObj['messages'] = [f"Rooms available for booking Room-Type: {room_type}, Date-Time: {room_booking_slot_datetime}."]
                rspDataObj['data'] = {
                    "available_rooms": availableRoomsDetails
                }
            else:
                rspDataObj['status_code'] = 404
                rspDataObj['messages'] = [f"No rooms available for booking Room-Type: {room_type}, Date-Time: {room_booking_slot_datetime}."]
    except Exception as e:
        print(f"Exception error occured: {e}")
        rspDataObj['status_code'] = 500
        rspDataObj['messages'] = [f"Error occured: {str(e)}"]

    return JSONResponse(status_code=rspDataObj['status_code'], content=rspDataObj)


