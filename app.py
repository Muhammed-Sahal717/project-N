import os
from datetime import datetime, timedelta, timezone

import jwt
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY", "dev-only-secret-change-me")
app.config["DEMO_USERNAME"] = os.environ.get("DEMO_USERNAME", "demo")
app.config["DEMO_PASSWORD"] = os.environ.get("DEMO_PASSWORD", "demo123")
app.config["TOKEN_TTL_MINUTES"] = int(os.environ.get("TOKEN_TTL_MINUTES", "15"))


def create_token(username: str) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        "sub": username,
        "iat": now,
        "exp": now + timedelta(minutes=app.config["TOKEN_TTL_MINUTES"]),
    }
    return jwt.encode(payload, app.config["SECRET_KEY"], algorithm="HS256")


def decode_token(token: str) -> dict:
    return jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])


@app.get("/")
def index():
    return render_template("index.html")


@app.post("/login")
def login():
    data = request.get_json(silent=True) or {}
    username = data.get("username", "")
    password = data.get("password", "")

    if username != app.config["DEMO_USERNAME"] or password != app.config["DEMO_PASSWORD"]:
        return jsonify({"error": "Invalid demo credentials."}), 401

    token = create_token(username)
    return jsonify(
        {
            "message": "Login successful.",
            "token": token,
            "token_type": "Bearer",
            "expires_in_minutes": app.config["TOKEN_TTL_MINUTES"],
        }
    )


@app.get("/protected")
def protected():
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        return jsonify({"error": "Missing bearer token."}), 401

    token = auth_header.removeprefix("Bearer ").strip()
    if not token:
        return jsonify({"error": "Missing bearer token."}), 401

    try:
        payload = decode_token(token)
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token has expired."}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "Token is invalid."}), 401

    return jsonify(
        {
            "message": "Protected data accessed successfully.",
            "subject": payload.get("sub"),
            "issued_at": payload.get("iat"),
            "expires_at": payload.get("exp"),
        }
    )


if __name__ == "__main__":
    app.run(debug=True)
