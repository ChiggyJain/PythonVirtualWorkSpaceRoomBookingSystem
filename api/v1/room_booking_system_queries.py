

import uuid
import aiomysql
from typing import Optional
from core.mysql_db import MysqlDB


async def getTeamsDetails(teamId: Optional[int] = None):

    """
        This function is used to get all teams with member count details
    """
    
    rspDataObj = {
        "status_code": 400,
        "messages": [],
        "data": {}
    }

    try:

        sqlQry = """
            SELECT 
            t.id teamId,
            t.team_name teamName,
            COUNT(DISTINCT tm.user_id) teamMembersCount
            FROM TEAM_MEMBERS tm
            JOIN TEAMS t ON t.id=tm.team_id
            JOIN USERS u ON u.id=tm.user_id
            WHERE 1
        """

        params = []

        # Conditionally add teamId filter
        if teamId is not None and teamId>0:
            sqlQry+= " AND t.id = %s "
            params.append(teamId)
        
        sqlQry+= " GROUP BY t.id "
        
        async with MysqlDB.pool.acquire() as conn:
            await conn.begin() 
            await conn.autocommit(True)
            async with conn.cursor(aiomysql.DictCursor) as cur:
                await cur.execute(sqlQry, params)
                availableTeamMembersDetails = await cur.fetchall()
                #print(f"DB-Extracted-Teams-Available-Details: {availableTeamMembersDetails}")
                if availableTeamMembersDetails and len(availableTeamMembersDetails)>0:
                    rspDataObj['status_code'] = 200
                    rspDataObj['messages'] = [f"Team with members details is found."]
                    rspDataObj['data'] = {
                        "teams": availableTeamMembersDetails
                    }
                else:
                    rspDataObj['status_code'] = 200
                    rspDataObj['messages'] = [f"No team detare found."]
                
    except Exception as e:
        print(f"Exception error occured: {e}")
        rspDataObj['status_code'] = 500
        rspDataObj['messages'] = [f"Error occured: {str(e)}"]
    return rspDataObj



async def getAvailableRoomsDetails(room_type:str, room_booking_slot_datetime: str):

    """
        This function is used to get all available rooms based on given room_type, datetime slot
    """
    
    rspDataObj = {
        "status_code": 400,
        "messages": [],
        "data": {}
    }

    try:

        sqlQry = """
            SELECT 
            r.id AS roomId,
            r.room_name AS roomName,
            r.room_type AS roomType,
            COALESCE(room_capacity, 0) AS roomSeatCapacity,
            COALESCE(b.booked_count, 0) AS roomSeatBookedCount,
            COALESCE((COALESCE(room_capacity, 0) - COALESCE(b.booked_count, 0)), 0) roomSeatBookingAvailableCount
            FROM ROOMS r
            LEFT JOIN (
                SELECT 
                room_id, 
                COUNT(*) AS booked_count
                FROM BOOKINGS
                WHERE 1
                AND status='Booked'
                AND %s BETWEEN booked_start_datetime_slot AND booked_end_datetime_slot
                GROUP BY room_id
            ) b ON r.id=b.room_id
            WHERE 1
            AND r.room_type=%s
            AND (
                (r.room_type IN ('Private', 'Conference') AND COALESCE(b.booked_count, 0) = 0)
                    OR 
                (r.room_type='Shared-Desk' AND COALESCE(b.booked_count, 0)<r.room_capacity)
            )
        """
        
        async with MysqlDB.pool.acquire() as conn:
            await conn.begin() 
            await conn.autocommit(True)
            async with conn.cursor(aiomysql.DictCursor) as cur:
                #print(f"room_type: {room_type}, room_booking_slot_datetime: {room_booking_slot_datetime}\n")
                await cur.execute(sqlQry, (room_booking_slot_datetime, room_type))
                availableRoomsDetails = await cur.fetchall()
                print(f"DB-Extracted-Rooms-Available-Details: {availableRoomsDetails}")
                if availableRoomsDetails and len(availableRoomsDetails)>0:
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
    return rspDataObj



async def cancelBookedRoomBookingDetails(user_id: int, room_booking_id: str):

    """
        This function is used to cancel booked room booking based on given user_id, room_booking_id
    """
    
    sqlQry = """
        UPDATE BOOKINGS b
        SET 
        b.status='Cancelled',
        b.updater_id = %s
        WHERE 1
        AND b.booked_id = %s
        AND b.creater_id = %s
        AND b.status='Booked'
    """

    async with MysqlDB.pool.acquire() as conn:
        async with conn.cursor(aiomysql.DictCursor) as cur:
            await cur.execute(sqlQry, (user_id, room_booking_id, user_id))
            await conn.commit()
            if cur.rowcount>0:
                print(f"Room booking-id {room_booking_id} is cancelled successfully.")
                return True
            else:
                print(f"No room booking found to cancel for user {user_id}.")
                return False
            


async def createRoomBookingDetails(user_id: int, team_id: int, room_id: int, room_booking_datetime_slot: str):

    """
        This function is used to book room using user_id, team_id, room_id, room_booking_datetime_slot slot
    """
    
    # standard response data object
    rspDataObj = {
        "status_code": 409,
        "messages": [],
        "data": {}
    }

    try:
        async with MysqlDB.pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cur:

                # Start transaction
                await cur.execute("START TRANSACTION;")

                # Lock any existing bookings for the room at that time
                selectQry = """
                    SELECT 
                    b.*
                    FROM BOOKINGS b
                    WHERE 1
                    AND b.status='Booked'
                    AND b.room_id = %s
                    AND b.booked_start_datetime_slot = %s
                    AND b.booked_end_datetime_slot = %s
                    FOR UPDATE
                """
                await cur.execute(selectQry, (room_id, room_booking_datetime_slot, room_booking_datetime_slot))
                existing_booking = await cur.fetchone()
                if existing_booking:
                    await conn.rollback()
                    rspDataObj['status_code'] = 409
                    rspDataObj['messages'] = [f"Room already booked for this slot. Room-ID: {room_id}, Slot: {room_booking_datetime_slot}"]
                    return rspDataObj
                
                # Insert the booking
                roomBookingUniqId = str(uuid.uuid4())
                roomBookingReferenceType = "USERS"
                roomBookingReferenceTypeId = user_id
                if team_id>0:
                    roomBookingReferenceType = "TEAMS"
                    roomBookingReferenceTypeId = team_id
                insert_query = """
                    INSERT INTO BOOKINGS (
                        booked_id,
                        room_id,
                        booked_start_datetime_slot,
                        booked_end_datetime_slot,
                        booked_reference_type,
                        booked_reference_type_id,
                        creater_id,
                        status
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s, 'Booked')
                """
                await cur.execute(insert_query, (
                    roomBookingUniqId,
                    room_id,
                    room_booking_datetime_slot,
                    room_booking_datetime_slot,
                    roomBookingReferenceType,
                    roomBookingReferenceTypeId,
                    user_id
                ))

                # getting last inserted record id
                last_inserted_id = cur.lastrowid
                if last_inserted_id>0:
                    # commit transaction
                    await conn.commit()
                    rspDataObj['status_code'] = 200
                    rspDataObj['messages'] = [f"Room is booked successfully and Booking-ID: {roomBookingUniqId}."]
                    rspDataObj['data'] = {
                        "room_booking_id" : roomBookingUniqId
                    }
                else:
                    await conn.rollback()
                    rspDataObj['status_code'] = 409
                    rspDataObj['messages'] = ["Room is not booked."]
                    rspDataObj['data'] = {}

    except Exception as e:
        print(f"Exception error occured: {e}")
        rspDataObj['status_code'] = 500
        rspDataObj['messages'] = [f"Error occured: {str(e)}"]
   
    return rspDataObj



async def getRoomBookingListDetails(user_id: int):

    """
        This function is used to get all room booked/cancelled based on user_id
    """
    
    rspDataObj = {
        "status_code": 400,
        "messages": [],
        "data": {}
    }

    try:

        sqlQry = """
            SELECT 
            r.id AS roomId,
            r.room_name AS roomName,
            r.room_type AS roomType,
            COALESCE(room_capacity, 0) AS roomSeatCapacity,
            COALESCE(b.booked_count, 0) AS roomSeatBookedCount,
            COALESCE((COALESCE(room_capacity, 0) - COALESCE(b.booked_count, 0)), 0) roomSeatBookingAvailableCount
            FROM ROOMS r
            JOIN BOOKINGS b ON b.room_id=r.id
            WHERE 1
            AND b.creater_id=%s
        """
        
        async with MysqlDB.pool.acquire() as conn:
            await conn.begin() 
            await conn.autocommit(True)
            async with conn.cursor(aiomysql.DictCursor) as cur:
                await cur.execute(sqlQry, (user_id))
                roomBookingListDetails = await cur.fetchall()
                print(f"DB-Extracted-Rooms-Booking-List-Details: {roomBookingListDetails}")
                if roomBookingListDetails and len(roomBookingListDetails)>0:
                    rspDataObj['status_code'] = 200
                    rspDataObj['messages'] = [f"Room booking details are available for User-ID: {user_id}"]
                    rspDataObj['data'] = {
                        "room_booking_list": roomBookingListDetails
                    }
                else:
                    rspDataObj['status_code'] = 404
                    rspDataObj['messages'] = [f"No room booking details available for User-ID: {user_id}."]
                
    except Exception as e:
        print(f"Exception error occured: {e}")
        rspDataObj['status_code'] = 500
        rspDataObj['messages'] = [f"Error occured: {str(e)}"]
    return rspDataObj

