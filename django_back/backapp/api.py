from ninja import NinjaAPI
from .auth import CustomAuth
api = NinjaAPI()
@api.get("/hello")
def hello(request):
    return {"hello": "message"}

@api.get("/secure-hello", auth=CustomAuth())
def secure_hello(request):
    return {"secure_hello": "This is a secure message"}