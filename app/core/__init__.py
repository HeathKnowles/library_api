"""
Core package:
Holds configuration and security utilities like JWT, password hashing, and settings.
"""

from app.core.config import settings
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    get_current_user,
)

__all__ = [
    "settings",
    "hash_password",
    "verify_password",
    "create_access_token",
    "get_current_user",
]
