from fastapi import FastAPI
import os
from dotenv import load_dotenv
from google.cloud import pubsub_v1
import threading
import json
from agents.agent import get_agent
from fastapi import Depends
from auth import get_current_user
from fastapi.middleware.cors import CORSMiddleware
from database import create_db_and_tables, ChatHistory, User, SessionDep
from redis import Redis
import boto3
import fitz
import hashlib

load_dotenv()

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


# -----------------------------------------
# Helper: Chunk Text
# -----------------------------------------
def chunk_text(text, chunk_size=4000):
    """Split text into safe LLM-sized chunks."""
    return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]


# -----------------------------------------
# ANALYSIS PIPELINE (CHUNKED)
# -----------------------------------------
def summarize_chunk(chunk: str):
    """Summaries each chunk via LLM."""
    prompt = f"""
You are a Legal Document Chunk Summarizer.
Summarize the following part of a legal document factually,
without legal advice, no opinions.

Chunk:
---------------------
{chunk}
---------------------
"""
    res = get_agent()(prompt)
    return res.message["content"][0]["text"].strip()


def final_legal_analysis(chunk_summaries):
    """Runs the final combined analysis."""
    prompt = f"""
You are a Legal Document Intelligence Agent.

You will receive summarized chunks of a long legal document.
Using ONLY the information in those summaries, generate:

1. A complete overall summary
2. Identified Indian legal sections (IT Act, IPC, Constitution etc.)
3. Factual context/explanation for each section
4. Highlight red flags (ambiguities, missing data, contradictions)
5. Do NOT provide legal advice
6. End with: "Disclaimer: This is an automated analysis, not legal advice."

Chunk Summaries:
-------------------------
{json.dumps(chunk_summaries, indent=2)}
-------------------------
"""
    res = get_agent()(prompt)
    return res.message["content"][0]["text"].strip()


# -----------------------------------------
# Status Route
# -----------------------------------------
@app.get("/status")
async def check(user=Depends(get_current_user), session: SessionDep = None):

    print("RAW:", repr(app.state.mess))
    payload = json.loads(app.state.mess)
    file_key = payload["file_key"]

    # S3 Fetch
    bucket = os.getenv("AWS_BUCKET_NAME")
    obj = s3.get_object(Bucket=bucket, Key=file_key)
    content = obj["Body"].read()

    # Extract Text
    pdf = fitz.open(stream=content, filetype="pdf")
    pdf_text = "".join(page.get_text() for page in pdf)

    # Cache Key
    content_hash = hashlib.sha256(pdf_text.encode("utf-8")).hexdigest()
    cached = redis_client.get(content_hash)

    if cached:
        print("🚀 Cache HIT:", content_hash)
        app.state.mess = None
        return {"response": cached, "cache": True}

    print("❌ Cache MISS:", content_hash)

    # Create user if needed
    existing_user = session.get(User, user["email"])
    if not existing_user:
        session.add(User(email=user["email"]))
        session.commit()

    # -----------------------------
    # CHUNK PIPELINE
    # -----------------------------
    print("📌 Splitting PDF into chunks...")
    chunks = chunk_text(pdf_text)

    print(f"📄 Total Chunks: {len(chunks)}")

    chunk_summaries = []
    for index, chunk in enumerate(chunks):
        print(f"🔹 Summarizing Chunk {index + 1}/{len(chunks)}...")
        summary = summarize_chunk(chunk)
        chunk_summaries.append(summary)

    print("🔍 Running Final Legal Analysis...")
    final_output = final_legal_analysis(chunk_summaries)

    # Save to Redis
    redis_client.set(content_hash, final_output, ex=60 * 60 * 24)

    # Save in DB
    new_history = ChatHistory(
        user_email=user["email"],
        file_key=file_key,
        response=final_output
    )
    session.add(new_history)
    session.commit()

    # Reset pubsub message
    app.state.mess = None

    return {"response": final_output}


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
