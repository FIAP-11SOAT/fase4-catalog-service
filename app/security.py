from typing import Optional
from fastapi import Depends, Header, HTTPException, status


def require_admin(x_role: Optional[str] = Header(default=None, alias="X-Role")):
    if x_role is None or x_role.lower() != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin role required")
    return True
