from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from kafka import KafkaProducer
from fastapi.middleware.cors import CORSMiddleware
import json

app = FastAPI()

# Add CORS middleware to allow cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

class Message(BaseModel):
    message: str

# Initialize Kafka producer
producer = KafkaProducer(
    bootstrap_servers=['kafka:9092'],  # Replace with your Kafka server address if different
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

@app.post("/send-message/")
def send_message(message: Message):
    try:
        # Send message to Kafka topic
        producer.send('test_topic', value={'message': message.message})
        producer.flush()
        return {"message": "Message sent to Kafka", "data": message.message}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))




# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel
# from kafka import KafkaProducer
# from fastapi.middleware.cors import CORSMiddleware
# import json

# app = FastAPI()

# # Set up CORS middleware to allow requests from any origin
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # Allows all origins
#     allow_credentials=True,
#     allow_methods=["*"],  # Allows all methods
#     allow_headers=["*"],  # Allows all headers
# )

# class Message(BaseModel):
#     message: str

# producer = KafkaProducer(
#     bootstrap_servers=['kafka:9092'],
#     value_serializer=lambda v: json.dumps(v).encode('utf-8')
# )

# # Kafka consumer setup
# consumer = KafkaConsumer(
#     'test_topic',
#     bootstrap_servers=['kafka:9092'],
#     auto_offset_reset='earliest',
#     enable_auto_commit=True,
#     group_id='my-group',
#     value_deserializer=lambda x: json.loads(x.decode('utf-8'))
# )

# @app.post("/send-message/")
# def send_message(message: Message):
#     try:
#         producer.send('test_topic', value={'message': message.message})
#         producer.flush()
#         return {"message": "Message sent to Kafka", "data": message.message}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# @app.websocket("/ws")
# async def websocket_endpoint(websocket: WebSocket):
#     await websocket.accept()
#     try:
#         for msg in consumer:
#             await websocket.send_text(f"Message from Kafka: {msg.value['message']}")
#     except Exception as e:
#         await websocket.close(code=1001, reason=str(e))
