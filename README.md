# JWT Learning Demo

A tiny Flask app that shows the JWT lifecycle end to end:

- submit demo credentials on the browser page
- receive a signed JWT from `/login`
- send the token to `/protected`
- see the server verify the signature and expiration

## What this teaches

JWTs are not encrypted by default. The token is signed by the server so the client can present it later, and the server can verify that the payload was not tampered with.

This demo keeps the scope intentionally small:

- one hardcoded demo user
- one signing secret from the environment
- one protected endpoint
- one small browser UI

## Run it

Install dependencies:

```bash
pip install -r requirements.txt
```

Start the app:

```bash
python app.py
```

Open the local address shown in the terminal, then log in with:

- username: `demo`
- password: `demo123`

## Environment variables

- `JWT_SECRET_KEY`: signing secret for token creation and verification
- `DEMO_USERNAME`: demo login username, default `demo`
- `DEMO_PASSWORD`: demo login password, default `demo123`
- `TOKEN_TTL_MINUTES`: token lifetime in minutes, default `15`

## Flow

1. The browser sends credentials to `/login`.
2. The server signs a JWT containing `sub`, `iat`, and `exp`.
3. The browser stores the token only in page memory for the demo.
4. The browser sends the token back as `Authorization: Bearer <token>`.
5. The server verifies the signature and expiration before returning protected data.

## Notes

This is a learning demo, not a production authentication system. It does not include password hashing, refresh tokens, persistent users, CSRF protection, or role-based access control.
