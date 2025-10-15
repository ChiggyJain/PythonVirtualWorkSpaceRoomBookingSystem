

import aiomysql
from core.mysql_db import MysqlDB



async def getAvailableRoomsDetails(room_type:str, room_booking_slot_datetime: str):

    """
        This function is used to get all available rooms based on given room_type, datetime slot
    """
    
    sqlQry = """
        SELECT 
        r.id roomId,
        r.room_name roomName,
        r.room_type roomType,
        r.room_capacity roomCapacity 
        FROM ROOMS r
        WHERE 1
        AND r.room_type = %s
        AND r.id NOT IN (
            SELECT 
            b.room_id
            FROM BOOKINGS b
            WHERE 1
            AND %s BETWEEN b.booked_start_datetime_slot AND b.booked_end_datetime_slot
        )
    """

    async with MysqlDB.pool.acquire() as conn:
        async with conn.cursor(aiomysql.DictCursor) as cur:
            await cur.execute(sqlQry, (room_type, room_booking_slot_datetime))
            roomsDetails = await cur.fetchall()
            print(f"DB-Extracted-Rooms-Available-Details: {roomsDetails}")
            if roomsDetails and len(roomsDetails)>0:
                return roomsDetails
            else:
                return False
