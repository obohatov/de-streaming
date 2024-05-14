from fastapi import FastAPI
from .producer import KafkaProducerManager
import os

app = FastAPI()
producer = KafkaProducerManager(
    bootstrap_servers=os.getenv("KAFKA_BOOTSTRAP_SERVERS", "127.0.0.1:9092")
)

@app.post("/data")
async def data(user_data: dict):
    try:
        producer.send("shop_data", user_data)
        return {"status": "ok"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
    