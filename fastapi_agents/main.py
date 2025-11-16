from fastapi import FastAPI 
import os
from dotenv import load_dotenv
from google.cloud import pubsub_v1
import threading
from concurrent.futures import TimeoutError
app = FastAPI()
@app.get("/hello")
async def hello():
    return {"message": "Hello, World!"}

def pubsub_listener():
  load_dotenv()
  credentials_path= os.getenv("GCP_CREDENTIALS_PATH")
  os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path
  subscriber = pubsub_v1.SubscriberClient()
  subscription_path=os.getenv("SUBSCRIBER_PATH")
  def callback(message: pubsub_v1.subscriber.message.Message):
        print(f"Received: {message.data.decode('utf-8')}")
        message.ack()
  print(f"Pub/Sub: Listening on {subscription_path}...")
  streaming_pull_feature = subscriber.subscribe(subscription_path, callback=callback)
  try:
      streaming_pull_feature.result()
  except Exception as e:
      print(f"Crashed: {e}")

@app.on_event("startup")
def launch_subscriber():
    thread = threading.Thread(target=pubsub_listener, daemon=True)
    thread.start()
    print("🎉 Pub/Sub listener running in background thread!")