#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound

from user import Base, User


class DB:
    """The DB instance
    """

    def __init__(self) -> None:
        """Initialize the DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """The add_user method for adding a user
        """
        new_user = User(email=email, hashed_password=hashed_password)
        # Create the new user
        self._session.add(new_user)
        # Save to db
        self._session.commit()
        return new_user

    def find_user_by(self, **kwargs) -> User:
        """Method for finding a user
        """
        if not kwargs:
            raise InvalidRequestError
        # Get the user from the database
        user = self._session.query(User).filter_by(**kwargs).first()
        if not user:
            # User was not found/ doesn't exist
            raise NoResultFound
        return user

    def update_user(self, user_id: int, **kwargs) -> None:
        """Method to update a user details
        """
        user = self.find_user_by(id=user_id)
        for key, value in kwargs.items():
            if not hasattr(user, key):
                raise ValueError
            setattr(user, key, value)
        # Save to db
        self._session.commit()
        return None
