# Import necessary modules
from fastapi import FastAPI, Response
from app.user.user import router as user_router

# Create the FastAPI application instance
app = FastAPI()


# Define the root endpoint
@app.get("/")
def root():
    # Return a simple response for server status check
    return Response("Server is running.")


# Include the user router in the main app
app.include_router(user_router)
