from fastapi import FastAPI, Depends
from stomp import Connection
from mq_connection import get_active_mq_connection
from command import router as command_router

app = FastAPI()

app.include_router(command_router, prefix="/commands")


@app.on_event("startup")
async def startup_event(connection: Connection = Depends(get_active_mq_connection)):
    print("Connected to ActiveMQ.")


@app.get("/")
async def root():
    return {"message": "Hello World"}
