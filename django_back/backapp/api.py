from ninja import NinjaAPI
from .auth import CustomAuth
from .schema import HelloTestResponse
api = NinjaAPI()
@api.get("/hello")
def hello(request):
    return {"hello": "message"}

@api.get("/secure-hello", auth=CustomAuth())
def secure_hello(request, payload: HelloTestResponse):
    return {"secure_hello": payload.text}