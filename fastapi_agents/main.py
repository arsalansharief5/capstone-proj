from fastapi import FastAPI 
import os
from dotenv import load_dotenv
from google.cloud import pubsub_v1
import threading
import json
from concurrent.futures import TimeoutError
from agents.agent import agent
from fastapi import Request as Req
from fastapi import Depends
from auth import get_current_user
app = FastAPI()
@app.get("/hello")
async def hello():
    return {"message": "Hello, World!"}
app.state.mess = None
def pubsub_listener():
  load_dotenv()
  credentials_path= os.getenv("GCP_CREDENTIALS_PATH")
  os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path
  subscriber = pubsub_v1.SubscriberClient()
  subscription_path=os.getenv("SUBSCRIBER_PATH")
  def callback(message: pubsub_v1.subscriber.message.Message):
        app.state.mess = message.data.decode('utf-8')
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

@app.get("/status")
async def check(req: Req, user = Depends(get_current_user)):
    print("RAW:", repr(app.state.mess))
    payload = json.loads(app.state.mess)
    print("File key: "+ payload["file_key"])
    query = f""" 
   You are a Legal Document Intelligence Agent.

Goals:
1. Extract and summarize the document using legal_mystic().
2. If the document references any legal sections (like Section 65 IT Act, Section 8, Article 21, etc) use:
   - fetch_india_act()
   - fetch_india_section()
   - fetch_constitution_article()
   to retrieve factual text from IndiaCode.
3. Provide a factual, concise legal context based on retrieved acts/articles.
4. DO NOT provide legal advice. Only factual interpretation.
5. Add red flags if the document has potential legal issues.
6. Add at the end:
   "Disclaimer: This is an automated analysis, not legal advice."
   Do this based on the document: "{payload["file_key"]}"
"""
    result = agent(query)
    text = result.message["content"][0]["text"]
    return {"response": text}