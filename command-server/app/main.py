from fastapi import FastAPI
from stomp import Connection

app = FastAPI()


def get_active_mq_connection():
    # Implement connection logic here
    connection = Connection([('localhost', 61613)])
    connection.connect(wait=True)
    return connection


@app.on_event("startup")
async def startup_event():
    active_mq_connection = get_active_mq_connection()
    print("Connected to ActiveMQ.")


@app.get("/")
async def root():
    return {"message": "Hello World"}
