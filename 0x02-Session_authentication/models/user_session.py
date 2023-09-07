#!/usr/bin/env python3
""" User session module
This module defines the UserSession class, which represents
a user's session.

It inherits from the Base class, which provides basic
functionality for database models.
"""

from models.base import Base


class UserSession(Base):
    """ UserSession class
    This class represents a user's session.

    Attributes:
        user_id (str): The ID of the associated user.
        session_id (str): The session ID.
    """

    def __init__(self, *args: list, **kwargs: dict):
        """ Initialize a UserSession instance
        Args:
            *args (list): Additional arguments (not used).
            **kwargs (dict): Keyword arguments.
        """
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get('user_id')
        self.session_id = kwargs.get('session_id')
