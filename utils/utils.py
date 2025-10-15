

import time
import uuid
from fastapi import FastAPI, HTTPException, Depends, status, Response, Cookie
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from jose import JWTError, jwt
from dotenv import load_dotenv
load_dotenv()
import os


# Configuration settings
JWT_SECRET_KEY=os.getenv("JWT_SECRET_KEY")
JWT_ALGORITHM=os.getenv("JWT_ALGORITHM")
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=int(os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES"))
JWT_REFRESH_TOKEN_EXPIRE_DAYS=int(os.getenv("JWT_REFRESH_TOKEN_EXPIRE_DAYS"))

print(f"JWT_SECRET_KEY: {JWT_SECRET_KEY}\n")
print(f"JWT_ALGORITHM: {JWT_ALGORITHM}\n")
print(f"JWT_ACCESS_TOKEN_EXPIRE_MINUTES: {JWT_ACCESS_TOKEN_EXPIRE_MINUTES}\n")
print(f"JWT_REFRESH_TOKEN_EXPIRE_DAYS: {JWT_REFRESH_TOKEN_EXPIRE_DAYS}\n")


def createLoginUserAccessToken(data: Dict[str, Any]) -> str:

    """
        Create a JWT access token for loging user details.
    """

    to_encode = data.copy()
    print(f"(Encoding string before expiring: {to_encode}\n")
    expire = (datetime.utcnow() + timedelta(minutes=JWT_ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    print(f"to_encode (after adding expiring-time): {to_encode}\n")
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    print(f"encoded_jwt: {encoded_jwt}\n")
    return encoded_jwt, expire


def decodeLoginUserAccessToken(token: str) -> str:

    """
        Decode a JWT token and return its payload.
    """

    token_data = None
    try:
        token_data = jwt.decode(token, JWT_SECRET_KEY, algorithms=JWT_ALGORITHM)
        print(f"Extracted data from access-token: {token}, decoded-data: {token_data}\n")
    except Exception as e:
        #token_data = str(e)
        token_data = None
    return token_data