
from fastapi import FastAPI
from api.v1.endpoints import router as v1_router
from core.mysql_db import MysqlDB


app = FastAPI(
    title="Virtual Workspace Room Booking System",
    version="1.0.0"
)

# include routers for API versions
app.include_router(v1_router, prefix="/api/v1")


@app.on_event("startup")
async def startup_event():
    print(f"Application startup: connecting to MySQL database...")
    await MysqlDB.connect()
    print(f"Application startup: connected to MySQL database...")

@app.on_event("shutdown")
async def shutdown_event():
    print(f"Application shutdown: disconnecting from MySQL database...")
    await MysqlDB.disconnect()
    print(f"Application shutdown: disconnected from MySQL database...")


# root endpoint
@app.get("/system-health", summary="System Health")
async def root():

    """
        This is api is used for checking backend system health
    """

    return {
        "message": "System is up and running successfully"
    }
