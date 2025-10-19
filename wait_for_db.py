

import asyncio
import aiomysql
import os

async def wait_for_db():
    db_host = os.getenv("MYSQL_DB_HOST")
    db_user = os.getenv("MYSQL_DB_USER")
    db_pass = os.getenv("MYSQL_DB_PASSWORD")
    db_name = os.getenv("MYSQL_DB_NAME")
    db_port = int(os.getenv("MYSQL_DB_PORT"))

    while True:
        try:
            conn = await aiomysql.connect(
                host=db_host,
                user=db_user,
                password=db_pass,
                db=db_name,
                port=db_port
            )
            conn.close()
            print("✅ MySQL is ready!")
            break
        except Exception as e:
            print("⏳ Waiting for MySQL...", str(e))
            await asyncio.sleep(3)

if __name__ == "__main__":
    asyncio.run(wait_for_db())
