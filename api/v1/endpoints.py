

from fastapi import APIRouter, Form, HTTPException, Depends 
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
async def login_user(loginUserRequestFormData: LoginRequest):

    """
        This api is used for authenticate user login details. 
        If login success then return access-token details with validity of 1000minutes only.
        If login success then use given acces-token for accessing other APIs.
        If login failed then return error messages.
        - **username**: Enter your account username
        - **password**: Enter your account password
    """

    # standard response data object
    rspDataObj = {
        "status_code": 401,
        "messages": [],
        "data": {}
    }

    try:

        authenticatedUsrLoginDetails = await getLoginUserDetails(loginUserRequestFormData.username, loginUserRequestFormData.password)
        print(f"authenticatedUsrLoginDetails: {authenticatedUsrLoginDetails}")
        if authenticatedUsrLoginDetails:
            accessTokenCreatedRspObj = createLoginUserAccessToken(data={"userId": authenticatedUsrLoginDetails['userId']}) 
            if accessTokenCreatedRspObj["status_code"] == 200:      
                rspDataObj['status_code'] = 200
                rspDataObj['messages'] = ["User login successfully."]
                rspDataObj['data'] = accessTokenCreatedRspObj['data']
            else:
                rspDataObj['messages'] = accessTokenCreatedRspObj['messages']
                rspDataObj['messages'].append(f"Unauthorized user accessing the system and access-token is not generated.")
        else:
            rspDataObj['status_code'] = 401
            rspDataObj['messages'] = ["Invalid username or password."]

    except Exception as e:
        print(f"Exception error occured: {e}")
        rspDataObj['status_code'] = 500
        rspDataObj['messages'] = [f"Error occured: {str(e)}"]

    return JSONResponse(status_code=rspDataObj['status_code'], content=rspDataObj)


# team with members count details api
@router.get("/teams/", summary="Team with members count details")
async def rooms_available(teamListRequestFormData: TeamsListRequest = Depends()):

    """
        This api is used for get team list with members count details.
        - **access_token**: Enter your account logged-in access token
    """

    # standard response data object
    rspDataObj = {
        "status_code": 404,
        "messages": [],
        "data": {}
    }

    try:

        # extracting request form data
        access_token = teamListRequestFormData.access_token

        # decoding access-token         
        decodedAccessTokenRspObj = decodeLoginUserAccessToken(access_token)
        print(f"decodedAccessTokenRspObj: {decodedAccessTokenRspObj}\n")
        if decodedAccessTokenRspObj['status_code']!=200:
            rspDataObj['status_code'] = 401
            rspDataObj['messages'] = ["Your account access token is expired. Please regenerate at your end via using /login api only"]
        if decodedAccessTokenRspObj['status_code']==200:
            userId = decodedAccessTokenRspObj['data']['token_data']["userId"]
            # fetching available rooms details
            availableTeamsDetailsRspObj = await getTeamsDetails()
            print(f"availableTeamsDetailsRspObj: {availableTeamsDetailsRspObj}")
            rspDataObj = availableTeamsDetailsRspObj

    except Exception as e:
        print(f"Exception error occured: {e}")
        rspDataObj['status_code'] = 500
        rspDataObj['messages'] = [f"Error occured: {str(e)}"]

    return JSONResponse(status_code=rspDataObj['status_code'], content=rspDataObj)



# rooms-available api
@router.get("/rooms/available", summary="Rooms Available for Booking")
async def rooms_available(roomAvailableRequestFormData: RoomsAvailableRequest = Depends()):

    """
        This api is used for check available rooms for booking on given access-token, room-type, date-time slot.
        - **access_token**: Enter your account logged-in access token
        - **room_type**: Enter your desired room type. Accepted room-types are 'Private', 'Conference', 'Shared-Desk'
        - **room_booking_slot_datetime**: Enter your desired booking slot datetime in 'YYYY-MM DD HH:MM' format  
    """

    # standard response data object
    rspDataObj = {
        "status_code": 404,
        "messages": [],
        "data": {}
    }

    try:

        # extracting request form data
        access_token = roomAvailableRequestFormData.access_token
        room_type = roomAvailableRequestFormData.room_type
        room_booking_slot_datetime = roomAvailableRequestFormData.room_booking_slot_datetime

        # validating room type details
        validatedRoomTypeRspObj = validateRoomType(room_type)
        if validatedRoomTypeRspObj["status_code"]!=200:
           return JSONResponse(status_code=validatedRoomTypeRspObj['status_code'], content=validatedRoomTypeRspObj)
        
        # validating room booking date-time slot details
        validatedRoomBookingSlotDateTimeRspObj = validateRoomBookingDateTimeSlot(room_booking_slot_datetime)
        if validatedRoomBookingSlotDateTimeRspObj["status_code"]!=200:
            return JSONResponse(status_code=validatedRoomBookingSlotDateTimeRspObj['status_code'], content=validatedRoomBookingSlotDateTimeRspObj)


        # decoding access-token         
        decodedAccessTokenRspObj = decodeLoginUserAccessToken(access_token)
        print(f"decodedAccessTokenRspObj: {decodedAccessTokenRspObj}\n")
        if decodedAccessTokenRspObj['status_code']!=200:
            rspDataObj['status_code'] = 401
            rspDataObj['messages'] = ["Your account access token is expired. Please regenerate at your end via using /login api only"]
        if decodedAccessTokenRspObj['status_code']==200:
            userId = decodedAccessTokenRspObj['data']['token_data']["userId"]
            # fetching available rooms details
            availableRoomsDetailsRspObj = await getAvailableRoomsDetails(room_type, room_booking_slot_datetime)
            print(f"availableRoomsDetailsRspObj: {availableRoomsDetailsRspObj}")
            rspDataObj = availableRoomsDetailsRspObj

    except Exception as e:
        print(f"Exception error occured: {e}")
        rspDataObj['status_code'] = 500
        rspDataObj['messages'] = [f"Error occured: {str(e)}"]

    return JSONResponse(status_code=rspDataObj['status_code'], content=rspDataObj)



# cancel-room-booking api
@router.post("/cancel/", summary="Cancel Booked Room Booking")
async def cancel_room_booking(cancelBookedRoomRequestFormData: CancelBookedRoomRequest):

    """
        This api is used for cancelling booked room booking.
        - **access_token**: Enter your account access token
        - **room_booking_id**: Enter your booked room booking id to cancel the booking
    """

    # standard response data object
    rspDataObj = {
        "status_code": 404,
        "messages": [],
        "data": {}
    }

    try:

        # extracting request form data
        access_token = cancelBookedRoomRequestFormData.access_token
        room_booking_id = cancelBookedRoomRequestFormData.room_booking_id

        # decoding access-token  
        decodedAccessTokenRspObj = decodeLoginUserAccessToken(access_token)       
        print(f"decodedAccessTokenRspObj: {decodedAccessTokenRspObj}\n")
        if decodedAccessTokenRspObj['status_code']!=200:
            rspDataObj['status_code'] = 401
            rspDataObj['messages'] = ["Your account access token is expired. Please regenerate at your end via using /login api only"]
        if decodedAccessTokenRspObj['status_code']==200:
            userId = decodedAccessTokenRspObj['data']['token_data']["userId"]
            # cancelling booked room booking
            cancelBookingStatus = await cancelBookedRoomBookingDetails(userId, room_booking_id)
            print(f"cancelBookingStatus: {cancelBookingStatus}")
            if cancelBookingStatus:
                rspDataObj['status_code'] = 200
                rspDataObj['messages'] = [f"Room booking id: {room_booking_id} is cancelled successfully."]
            else:
                rspDataObj['status_code'] = 404
                rspDataObj['messages'] = [f"Room booking id: {room_booking_id} not found or already cancelled."]

    except Exception as e:
        print(f"Exception error occured: {e}")
        rspDataObj['status_code'] = 500
        rspDataObj['messages'] = [f"Error occured: {str(e)}"]

    return JSONResponse(status_code=rspDataObj['status_code'], content=rspDataObj)



# room-booking api
@router.post("/bookings/", summary="Room booking")
async def room_booking(roomBookingRequestFormData: RoomBookingRequest):

    """
        This api is used for creating room booking details based on team/individual-user.
        - **access_token**: Enter your account access token
        - **team_id**: If you are booking room for TEAM then please provide team_id ELSE 0
        - **room_id**: Enter room id
        - **room_booking_slot_datetime**: Enter your desired booking slot datetime in 'YYYY-MM-DD HH:MM' format
    """

    # standard response data object
    rspDataObj = {
        "status_code": 404,
        "messages": [],
        "data": {}
    }

    try:

        # extracting request form data
        access_token = roomBookingRequestFormData.access_token
        team_id = roomBookingRequestFormData.team_id
        room_id = roomBookingRequestFormData.room_id
        room_booking_slot_datetime = roomBookingRequestFormData.room_booking_slot_datetime

        # validating room booking date-time slot details
        validatedRoomBookingSlotDateTimeRspObj = validateRoomBookingDateTimeSlot(room_booking_slot_datetime)
        if validatedRoomBookingSlotDateTimeRspObj["status_code"]!=200:
           return JSONResponse(status_code=validatedRoomBookingSlotDateTimeRspObj['status_code'], content=validatedRoomBookingSlotDateTimeRspObj) 
        

        # decoding access-token         
        decodedAccessTokenRspObj = decodeLoginUserAccessToken(access_token) 
        print(f"decodedAccessTokenRspObj: {decodedAccessTokenRspObj}\n")
        if decodedAccessTokenRspObj['status_code']!=200:
            rspDataObj['status_code'] = 401
            rspDataObj['messages'] = ["Your account access token is expired. Please regenerate at your end via using /login api only"]
        if decodedAccessTokenRspObj['status_code']==200:
            userId = decodedAccessTokenRspObj['data']['token_data']["userId"]
            # checking team members count details
            if team_id>0:
                teamRspObj = await getTeamsDetails(team_id)
                if teamRspObj['status_code'] == 200:
                    if teamRspObj['data']['teams'][0]['teamMembersCount']<3:
                        rspDataObj['status_code'] = 404
                        rspDataObj['messages'] = [f"Team-member-count is less than<3 in selected team-id. Not allowed to book conference room."]
                        return JSONResponse(status_code=rspDataObj['status_code'], content=rspDataObj)
            # room booking details
            roomBookedRspObj = await createRoomBookingDetails(userId, team_id, room_id, room_booking_slot_datetime)
            print(f"roomBookedRspObj: {roomBookedRspObj}")
            rspDataObj = roomBookedRspObj

    except Exception as e:
        print(f"Exception error occured: {e}")
        rspDataObj['status_code'] = 500
        rspDataObj['messages'] = [f"Error occured: {str(e)}"]

    return JSONResponse(status_code=rspDataObj['status_code'], content=rspDataObj)
