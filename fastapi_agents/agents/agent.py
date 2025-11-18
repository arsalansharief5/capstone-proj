from strands import Agent, tool
from strands.models.gemini import GeminiModel
import requests
import os
from dotenv import load_dotenv
import boto3
import fitz
load_dotenv()
model = GeminiModel(
    client_args={
        "api_key": os.getenv("GEMINI_API_KEY")
    },
    model_id="gemini-2.5-flash",
    params={
        "temperature": 0.5,
        "max_output_tokens": 2048,
        "top_p": 0.9,
        "top_k": 40
    }
)
s3 = boto3.client(
    's3', 
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"), 
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("COGNITO_REGION")
)

@tool
def legal_mystic(file_key: str):
    """Fetch the document from S3."""
    bucket = os.getenv("AWS_BUCKET_NAME")
    obj = s3.get_object(Bucket=bucket, Key=file_key)
    content = obj['Body'].read()
    pdf = fitz.open(stream=content, filetype="pdf")
    text = ""
    for page in pdf:
        text += page.get_text()
    return text

agent = Agent(model=model, tools=[legal_mystic])
