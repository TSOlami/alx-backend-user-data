#!/usr/bin/env python3
"""The app Module
"""


from flask import Flask, jsonify, request, abort, redirect
from auth import Auth

AUTH = Auth()

app = Flask(__name__)


@app.route('/', methods=['GET'])
def home() -> str:
    """Defines the home route

    Returns:
        JSON: A JSON response with a welcome message.
    """
    message = {"message": "Bienvenue"}
    return jsonify(message)


@app.route('/users', methods=['POST'])
def users() -> str:
    """Register a user.

    Returns:
        JSON: A JSON response indicating success or failure.
    """
    email = request.form.get('email')
    password = request.form.get('password')

    # Attempt to register the user
    try:
        user = AUTH.register_user(email, password)
        response = {
            "email": user.email,
            "message": "user created"
        }
        return jsonify(response), 200
    except Exception:
        # User already exists
        response = {"message": "email already registered"}
        return jsonify(response), 400


@app.route('/sessions', methods=['POST'])
def login() -> str:
    """Log in a user.

    Returns:
        JSON: A JSON response indicating success or failure.
    """
    email = request.form.get('email')
    password = request.form.get('password')
    # Authenticate the user
    if not (AUTH.valid_login(email, password)):
        abort(401)
    else:
        # Create a new session for the user
        session_id = AUTH.create_session(email)
        # Set the session ID as a cookie in the response
        response = jsonify({"email": email, "message": "logged in"})
        response.set_cookie('session_id', session_id)

    return response


@app.route('/sessions', methods=['DELETE'])
def logout() -> str:
    """Log out a user.

    Returns:
        JSON: A JSON response indicating success or failure.
    """
    # Extract the session ID from the request cookies
    session_id = request.cookies.get('session_id')
    # Find the user associated with the session ID
    user = AUTH.get_user_from_session_id(session_id)
    if not user:
        # User not found (invalid session ID)/Forbidden
        abort(403)
    # Destroy the session
    AUTH.destroy_session(user.id)
    # Redirect the user to GET /
    return redirect('/')


@app.route('/profile', methods=['GET'])
def profile() -> str:
    """Get a user Profile
    """
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        # Respond with a 200 status code and a JSON payload
        return jsonify({"email": user.email}), 200
    else:
        # Forbidden
        abort(403)


@app.route('/reset_password', methods=['POST'])
def get_reset_password_token() -> str:
    """Get a reset password token for a user.

    Returns:
        JSON: A JSON response indicating success or failure.
    """
    # Extract the email field from the form data in the request
    email = request.form.get('email')
    try:
        # Check if the email is registered and generate a token
        reset_token = AUTH.get_reset_password_token(email)
        # Respond with a 200 status code and a JSON payload
        response = {
                "email": email,
                "reset_token": reset_token
            }
        return jsonify(response), 200
    except Exception:
        # Email not registered/Forbidden
        abort(403)


@app.route('/reset_password', methods=['PUT'])
def update_password() -> str:
    """Update the user's password using a reset token.

    Returns:
        JSON: A JSON response indicating success or failure.
    """
    # Extract the fields from the form data in the request
    email = request.form.get('email')
    reset_token = request.form.get('reset_token')
    new_password = request.form.get('new_password')
    try:
        # Update the user's password with the new password
        AUTH.update_password(reset_token, new_password)
        response = {
                "email": email,
                "message": "Password updated"
            }
        return jsonify(response), 200
    except Exception:
        # Invalid reset token/ Forbidden
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
