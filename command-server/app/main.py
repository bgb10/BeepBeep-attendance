from fastapi import FastAPI, Depends
from stomp import Connection
from mq_connection import get_active_mq_connection

app = FastAPI()



@app.on_event("startup")
async def startup_event(connection: Connection = Depends(get_active_mq_connection)):
    print("Connected to ActiveMQ.")


@app.get("/")
async def root():
    return {"message": "Hello World"}
