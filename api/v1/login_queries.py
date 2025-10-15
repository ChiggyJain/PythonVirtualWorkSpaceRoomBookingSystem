
import aiomysql
import hashlib  
from core.mysql_db import MysqlDB

async def getLoginUserDetails(username: str, password: str):

    """
        This function is used to authenticate user login details
    """
    
    sqlQry = """
        SELECT
        u.id userId,
        u.name userFullName 
        FROM USERS u
        WHERE 1 
        AND u.username=%s 
        AND u.userpassword=%s
    """
    async with MysqlDB.pool.acquire() as conn:
        async with conn.cursor(aiomysql.DictCursor) as cur:
            print(f"Login-User-Pwd-Md5-String: {hashlib.md5(password.encode()).hexdigest()}")
            await cur.execute(sqlQry, (username, hashlib.md5(password.encode()).hexdigest()))
            loginUserDetails = await cur.fetchall()
            print(f"DB-Extracted-Login-User-Details: {loginUserDetails}")
            if loginUserDetails and len(loginUserDetails)==1:
                return loginUserDetails[0]
            else:
                return False
