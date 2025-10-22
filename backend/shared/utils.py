from typing import Optional, Dict, Any
from fastapi import HTTPException, status

def parse_bearer_token(authorization: Optional[str]) -> str:
    """
    Extracts bearer token from Authorization header string.
    Raises 401 if header is missing or malformed.
    """
    if not authorization:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authorization header missing")
    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authorization header")
    return parts[1]


def token_has_role(payload: Dict[str, Any], role: str) -> bool:
    r = payload.get("role") or payload.get("roles")
    if isinstance(r, list):
        return any(str(x).lower() == role.lower() for x in r)
    return bool(r and str(r).lower() == role.lower())