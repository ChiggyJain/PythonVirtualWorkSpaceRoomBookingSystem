

from fastapi import APIRouter, Form
from api.v1.schemas import *
from datetime import datetime

router = APIRouter()


# loging api
@router.post("/login/", summary="User Login Authentication")
def user_login(loginRequestFormData: LoginRequest):

    """
        This api is used for authenticate user login details. 
        If login success then return access-token details with validity of 15minutes only.
        If login failed then return error messages.
        - **username**: Enter your account username 
        - **password**: Enter your account password
    """

    return {
        "message": f"User {loginRequestFormData.username} logged in successfully"
    }
