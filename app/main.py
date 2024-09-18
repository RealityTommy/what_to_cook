from fastapi import FastAPI, Response

app = FastAPI()

# Server Status
@app.get("/")
def root():
    return Response("Server is running.")