
from fastapi import FastAPI
from api.v1.endpoints import router as v1_router


app = FastAPI(
    title="Virtual Workspace Room Booking System",
    version="1.0.0"
)

# include routers for API versions
app.include_router(v1_router, prefix="/api/v1")


# root endpoint
@app.get("/", summary="Backend System Entry Point")
def root():

    """
        This is backend system entry point
    """

    return {
        "message": "Welcome to Virtual Workspace Room Booking System REST APIs"
    }
