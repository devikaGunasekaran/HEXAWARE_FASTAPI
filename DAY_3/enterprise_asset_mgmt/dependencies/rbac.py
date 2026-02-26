from fastapi import Depends, HTTPException, status
from services.auth_service import get_current_active_user
from models.user import User, UserRole

def allow_roles(*roles: str):
    def role_checker(current_user: User = Depends(get_current_active_user)):
        if current_user.role not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Operation not permitted for your role"
            )
        return current_user
    return role_checker
