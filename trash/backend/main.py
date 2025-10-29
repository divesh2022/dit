from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from datetime import timedelta

from backend.services.auth import AuthService
from backend.routers import student, faculty

app = FastAPI(title="DIT Backend")

# Include routers
app.include_router(student.router)
app.include_router(faculty.router)


class TokenRequest(BaseModel):
    username: str
    role: str = "student"
    user_id: int
    expires_minutes: Optional[int] = 60


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


@app.post("/auth/token", response_model=TokenResponse)
def create_token(req: TokenRequest):
    """
    Simple token endpoint for development/demo.
    In production you should validate credentials and issue tokens securely.
    """
    payload = {
        "sub": req.user_id,
        "username": req.username,
        "role": req.role
    }
    token = AuthService.create_access_token(payload, expires_delta=timedelta(minutes=req.expires_minutes))
    if not token:
        raise HTTPException(status_code=500, detail="Failed to create token")
    return {"access_token": token, "token_type": "bearer"}


@app.get("/")
def root():
    return {"status": "ok"," message": "DIT Backend is running."}