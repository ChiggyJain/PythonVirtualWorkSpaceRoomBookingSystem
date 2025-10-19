

import time
import uuid
from fastapi import FastAPI, HTTPException, Depends, status, Response, Cookie
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from datetime import datetime, timedelta
from datetime import time as dt_time  # rename to avoid clash
from typing import Optional, Dict, Any
from jose import JWTError, jwt
from dotenv import load_dotenv
load_dotenv()
import os


# Configuration settings
JWT_SECRET_KEY=os.getenv("JWT_SECRET_KEY")
JWT_ALGORITHM=os.getenv("JWT_ALGORITHM")
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=int(os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES"))
JWT_REFRESH_TOKEN_EXPIRE_DAYS=int(os.getenv("JWT_REFRESH_TOKEN_EXPIRE_DAYS"))

print(f"JWT_SECRET_KEY: {JWT_SECRET_KEY}\n")
print(f"JWT_ALGORITHM: {JWT_ALGORITHM}\n")
print(f"JWT_ACCESS_TOKEN_EXPIRE_MINUTES: {JWT_ACCESS_TOKEN_EXPIRE_MINUTES}\n")
print(f"JWT_REFRESH_TOKEN_EXPIRE_DAYS: {JWT_REFRESH_TOKEN_EXPIRE_DAYS}\n")


def createLoginUserAccessToken(data: Dict[str, Any]) -> str:

    """
        Create a JWT access token for loging user details.
    """

    rspDataObj = {
        "status_code": 400,
        "messages": [],
        "data": {}
    }

    try:

        to_encode = data.copy()
        print(f"(Encoding string before expiring: {to_encode}\n")
        expire = (datetime.now() + timedelta(minutes=JWT_ACCESS_TOKEN_EXPIRE_MINUTES))
        to_encode.update({"exp": expire})
        print(f"to_encode (after adding expiring-time): {to_encode}\n")
        encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
        print(f"encoded_jwt: {encoded_jwt}\n")
        rspDataObj['status_code'] = 200
        rspDataObj['messages'] = [f"Access token is created successfully."]
        rspDataObj['data'] = {
            "token_type": "bearer",
            "access_token": encoded_jwt,
            "access_token_expire_time" : str(expire)
        }
    
    except Exception as e:
        print(f"Exception error occured: {e}")
        rspDataObj['status_code'] = 500
        rspDataObj['messages'] = [f"Error occured: {str(e)}"]

    return rspDataObj



def decodeLoginUserAccessToken(token: str) -> str:

    """
        Decode a JWT token and return its payload.
    """

    rspDataObj = {
        "status_code": 400,
        "messages": [],
        "data": {}
    }

    try:
        
        token_data = jwt.decode(token, JWT_SECRET_KEY, algorithms=JWT_ALGORITHM)
        print(f"Extracted data from access-token: {token}, decoded-data: {token_data}\n")
        rspDataObj['status_code'] = 200
        rspDataObj['messages'] = [f"Access token is decoded successfully."]
        rspDataObj['data'] = {
            "token_data": token_data
        }

    except Exception as e:
        print(f"Exception error occured: {e}")
        rspDataObj['status_code'] = 500
        rspDataObj['messages'] = [f"Error occured: {str(e)}"]

    return rspDataObj




def validateRoomType(room_type: str):
    rspDataObj = {
        "status_code": 400,
        "messages": [],
        "data": {}
    }
    try:

        if room_type not in ['Private', 'Conference', 'Shared-Desk']:
            rspDataObj['status_code'] = 400
            rspDataObj['messages'] = [f"Invalid room-type: {room_type}. Accepted room-types are 'Private', 'Conference', 'Shared-Desk'."]
        else:
            rspDataObj['status_code'] = 200
            rspDataObj['messages'] = [f"Room type is valid'."]

    except Exception as e:
        print(f"Exception error occured: {e}")
        rspDataObj['status_code'] = 500
        rspDataObj['messages'] = [f"Error occured: {str(e)}"]

    return rspDataObj


def validateRoomBookingDateTimeSlot(room_booking_slot_datetime: str):
    rspDataObj = {
        "status_code": 400,
        "messages": [],
        "data": {}
    }
    try:

        if room_booking_slot_datetime:
            # Parse string to datetime object
            slot_dt = datetime.strptime(room_booking_slot_datetime, "%Y-%m-%d %H:%M:%S")
            # Check if the slot is not in the past
            if slot_dt < datetime.now():
                rspDataObj['status_code'] = 400
                rspDataObj['messages'] = ["Slot datetime cannot be in the past."]
                return rspDataObj
            # Check if time is within allowed working hours
            if not (dt_time(9, 0) <= slot_dt.time() <= dt_time(18, 0)):
                rspDataObj['status_code'] = 400
                rspDataObj['messages'] = ["Slot time must be between 09:00 and 18:00."]
                return rspDataObj
            # Check if minute is zero (hourly slot)
            if slot_dt.minute != 0 or slot_dt.second != 0:
                rspDataObj['status_code'] = 400
                rspDataObj['messages'] = ["Slot must be on the hour, e.g: 10:00, 11:00."]
                return rspDataObj
            rspDataObj['status_code'] = 200
            rspDataObj['messages'] = ["Given date-time slot is valid."]

    except Exception as e:
        print(f"Exception error occured: {e}")
        rspDataObj['status_code'] = 500
        rspDataObj['messages'] = [f"Error occured: {str(e)}"]

    return rspDataObj

