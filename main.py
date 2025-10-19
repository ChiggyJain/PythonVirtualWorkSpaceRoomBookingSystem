

import asyncio
from fastapi import FastAPI
from api.v1.endpoints import router as v1_router
from core.mysql_db import MysqlDB

# app instance
app = FastAPI(
    title="Virtual Workspace Room Booking System",
    version="1.0.0"
)

# include routers for API versions example: v1, v2 etc.
app.include_router(v1_router, prefix="/api/v1")


# app startup events
# database open connections
@app.on_event("startup")
async def startup_event():
    print(f"Application startup: connecting to MySQL database...\n")
    RETRY_INTERVAL = 3
    MAX_RETRIES = 20
    retries = 0
    while retries < MAX_RETRIES:
        try:
            await MysqlDB.connect()
            print("Application startup: connected to MySQL database...\n")
            break
        except Exception as e:
            retries+= 1
            print(f"Waiting for MySQL... attempt {retries}/{MAX_RETRIES}, error: {e}\n")
            await asyncio.sleep(RETRY_INTERVAL)
    else:
        raise RuntimeError("Could not connect to MySQL after multiple attempts")


# app hutdown events
# database close connections
@app.on_event("shutdown")
async def shutdown_event():
    print(f"Application shutdown: disconnecting from MySQL database...\n")
    await MysqlDB.disconnect()
    print(f"Application shutdown: disconnected from MySQL database...\n")



# system-health endpoint
@app.get("/system-health", summary="System Health")
async def root():

    """
        This api is used for checking backend system health
    """

    return {
        "message": "System is up and running successfully"
    }
