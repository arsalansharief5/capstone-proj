from ninja.security import HttpBearer
import os
from dotenv import load_dotenv
import json
from jose import jwk, jwt
from jose.utils import base64url_decode
from datetime import datetime
import requests
load_dotenv()
COGNITO_REGION = os.getenv("COGNITO_REGION")
USER_POOL_ID = os.getenv("USER_POOL_ID")
USER_POOL_CLIENT_ID = os.getenv("USER_POOL_CLIENT_ID")
JWKS_URL = f"https://cognito-idp.{COGNITO_REGION}.amazonaws.com/{USER_POOL_ID}/.well-known/jwks.json"
JWKS = requests.get(JWKS_URL).json()["keys"]
def validate_token(token: str):
    headers = jwt.get_unverified_headers(token)
    kid = headers['kid']
    jwt_key = next((key for key in JWKS if key['kid']==kid), None)
    if jwt_key is None:
        raise Exception("Public key not found in JWKS")
    unverified = jwt.get_unverified_claims(token)
    if unverified["exp"] < datetime.utcnow().timestamp():
        raise Exception("Token is expired")
    if unverified["aud"] != COGNITO_USER_POOL_CLIENT_ID:
        raise Exception("Token was not issued for this audience")
    public_key = jwt.construct(jwt_key)
    message, encoded_signature = token.rsplit('.', 1)
    decoded_signature = base64url_decode(encoded_signature.encode())
    return unverified

class CustomAuth(HttpBearer):
    def authenticate(self, request, token):
        try:
            claims = validate_token(token)
            return claims
        except Exception as e: 
            return e