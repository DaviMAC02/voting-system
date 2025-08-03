import os
import jwt
from flask import request, g
from app.modules.users.models import User

SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")


def authenticate_user():
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return False, {"message": "Missing or invalid token"}, 401

    token = auth_header.split(" ")[1]
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])

        g.user = User.query.filter_by(id=payload["identity"]).first()
        if not g.user:
            return False, {"message": "User not found"}, 404
        return True, None, None
    except jwt.ExpiredSignatureError:
        return False, {"message": "Token expired"}, 401
    except jwt.InvalidTokenError:
        return False, {"message": "Invalid token"}, 401
