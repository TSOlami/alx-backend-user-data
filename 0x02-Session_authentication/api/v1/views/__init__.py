#!/usr/bin/env python3
"""
API Blueprint Configuration
"""

from flask import Blueprint

# Create a Blueprint for API version 1
app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")

# Import views from other modules
from api.v1.views.index import *
from api.v1.views.users import *
from api.v1.views.session_auth import *

# Load user data from a file
User.load_from_file()
