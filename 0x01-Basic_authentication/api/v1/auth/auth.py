#!/usr/bin/env python3
"""
Route module for auth
"""
from flask import request
from typing import List, TypeVar


class Auth():
    """Returns authentication
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Returns bool
        """
        return False

    def authorization_header(self, request=None) -> str:
        """Returns str
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Returns str
        """
        return None
