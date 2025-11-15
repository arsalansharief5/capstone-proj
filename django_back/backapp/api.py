from ninja import NinjaAPI
from .auth import CustomAuth
from .schema import HelloTestResponse, GetSignedUrl
import uuid, boto3
import os
from dotenv import load_dotenv
api = NinjaAPI()
load_dotenv()
s3 = boto3.client(
    's3', 
    region_name= os.getenv("COGNITO_REGION"),
    aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY"),
)
bucket_name = os.getenv("S3_BUCKET_NAME")

@api.post("/secure-hello", auth=CustomAuth())
def secure_hello(request, payload: HelloTestResponse):
    return {"secure_hello": payload.text}

@api.post("/get-upload-url", auth=CustomAuth())
def get_upload_url(request, payload: GetSignedUrl):
    user = request.auth
    user_id = user['sub']
    file_id = str(uuid.uuid4())
    key = f"videos/{user_id}/{file_id}-{payload.file_name}"
    presigned_url = s3.generate_presigned_url(
        ClientMethod = 'put_object', 
        Params = {
            'Bucket': bucket_name, 
            "Key" : key, 
            "ContentType": payload.content_type
        }, 
        ExpiresIn = 600
    )
    return {"upload_url": presigned_url, "file_key": key}
