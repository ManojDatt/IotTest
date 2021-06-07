# -*- coding: utf-8 -*-
import secrets
from fastapi import Depends, HTTPException, status as http_status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

security = HTTPBasic()

def has_access(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, "IOT@Snow")
    correct_password = secrets.compare_digest(credentials.password, "IOT@Snow12345")
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=http_status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )

def http_response(message="", code=200, data=dict(), error=""):
    return {'message': message, 'code': code, 'data': data, 'error': error}
