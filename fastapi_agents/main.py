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
from fastapi.middleware.cors import CORSMiddleware
from database import create_db_and_tables, ChatHistory, User, get_session, SessionDep
from redis import Redis
import boto3
import fitz

# Load .env (Docker environment variables are loaded automatically)
load_dotenv()
# credentials_path="C:\\Users\\HP\\Downloads\\capstone-proj\\django_back\\backapp\\keys.json"
# os.environ['GOOGLE_APPLICATION_CREDENTIALS']= credentials_path

# -----------------------------------------
# Redis + S3 Setup
# -----------------------------------------
redis_client = Redis(
    host=os.getenv("REDIS_URL"),
    port=int(os.getenv("REDIS_PORT")),
    password=os.getenv("REDIS_PASSWORD"),
    decode_responses=True
)

s3 = boto3.client(
    's3',
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("COGNITO_REGION")
)

# -----------------------------------------
# FastAPI App
# -----------------------------------------
app = FastAPI()

@app.get("/hello")
async def hello():
    return {"message": "Hello, World!"}

app.state.mess = None


# -----------------------------------------
# Pub/Sub Listener
# -----------------------------------------
def pubsub_listener():
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = os.getenv("SUBSCRIBER_PATH")

    def callback(message: pubsub_v1.subscriber.message.Message):
        app.state.mess = message.data.decode("utf-8")
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
    create_db_and_tables()
    thread = threading.Thread(target=pubsub_listener, daemon=True)
    thread.start()
    print("🎉 Pub/Sub listener running in background thread!")

def truncate(text, max_chars=5000):
    return text[:max_chars] + "..." if len(text) > max_chars else text

# -----------------------------------------
# Status Route
# -----------------------------------------
@app.get("/status")
async def check(user=Depends(get_current_user), session: SessionDep=None):
    print("RAW:", repr(app.state.mess))

    payload = json.loads(app.state.mess)
    print("File key:", payload["file_key"])

    existing_user = session.get(User, user["email"])
    bucket = os.getenv("AWS_BUCKET_NAME")
    obj = s3.get_object(Bucket=bucket, Key=payload["file_key"])

    content = obj["Body"].read()
    pdf = fitz.open(stream=content, filetype="pdf")

    pdf_text = ""
    for page in pdf:
        pdf_text += page.get_text()
    short_text = truncate(pdf_text)

    import hashlib
    content_hash = hashlib.sha256(pdf_text.encode("utf-8")).hexdigest()

    cached = redis_client.get(content_hash)
    if cached:
        print("🚀 Cache HIT:", content_hash)
        app.state.mess = None
        return {"response": cached, "cache": True}

    print("❌ Cache MISS:", content_hash)

    if not existing_user:
        session.add(User(email=user["email"]))
        session.commit()

    query = f""" 
   You are a Legal Document Intelligence Agent. 
Below is the FULL extracted text of a legal document.

Goals:
1. Summarize the document clearly.
2. Identify referenced Indian legal sections (like IT Act, Constitution).
3. Provide factual context for these sections.
4. Highlight legal red flags.
5. Do NOT provide legal advice.
6. End with: "Disclaimer: This is an automated analysis, not legal advice."

Extracted document text:
---------------------------
{short_text}
---------------------------
"""

    result = agent(query)
    text = result.message["content"][0]["text"]

    new_history = ChatHistory(
        user_email=user["email"],
        file_key=payload["file_key"],
        response=text
    )

    redis_client.set(content_hash, text, ex=60 * 60 * 24)
    session.add(new_history)
    session.commit()
    session.refresh(new_history)

    app.state.mess = None
    return {"response": text}


# -----------------------------------------
# CORS
# -----------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://capstone-proj-green.vercel.app",
        "http://localhost:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app = app 