#!/usr/bin/env python3
"""
Module for authentication using Session auth
"""

from .auth import Auth
from models.user import User
from uuid import uuid4


class SessionAuth(Auth):
    """
    Session Authentication Class
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        Creates a session ID for a user.

        Args:
            user_id (str, optional): The ID of the user. Defaults to None.

        Returns:
            str: The session ID.
        """
        if user_id is None or not isinstance(user_id, str):
            return None

        session_id = str(uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        Retrieves the user ID associated with a session ID.

        Args:
            session_id (str, optional): The session ID. Defaults to None.

        Returns:
            str: The user ID.
        """
        if session_id is None or not isinstance(session_id, str):
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """
        Retrieves the current user.

        Args:
            request (request object, optional): The request object.
            Defaults to None.
        """
        session_cookie = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_cookie)
        user = User.get(user_id)
        return user

    def destroy_session(self, request=None):
        """
        Destroys a session.

        Args:
            request (request object, optional): The request object.
            Defaults to None.

        Returns:
            bool: True if the session was destroyed, False otherwise.
        """
        if request is None:
            return False
        session_cookie = self.session_cookie(request)
        if session_cookie is None:
            return False
        user_id = self.user_id_for_session_id(session_cookie)
        if user_id is None:
            return False
        del self.user_id_by_session_id[session_cookie]
        return True
