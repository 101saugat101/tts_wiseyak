import os
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from urllib.parse import urlencode
import httpx
from dotenv import load_dotenv
from sqlalchemy import select, update, insert, func
from database.database import database, users, user_credits

# Load environment variables
load_dotenv()

# OAuth2 configuration from .env
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")
AUTH_URI = os.getenv("AUTH_URI")
TOKEN_URI = os.getenv("TOKEN_URI")
USERINFO_URI = os.getenv("USERINFO_URI")

# Define FastAPI router
router = APIRouter()


@router.get("/")
async def index():
    return HTMLResponse('<a href="/auth/login">Login with Google</a>')


@router.get("/login")
async def login():
    params = {
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "response_type": "code",
        "scope": "openid email profile",
        "access_type": "offline",
        "prompt": "consent"
    }
    url = f"{AUTH_URI}?{urlencode(params)}"
    return RedirectResponse(url)


@router.get("/callback")
async def auth_callback(request: Request):
    if not database.is_connected:
        await database.connect()

    code = request.query_params.get("code")
    if not code:
        return HTMLResponse("No authorization code provided.", status_code=400)

    # Exchange authorization code for access token
    data = {
        "code": code,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "redirect_uri": REDIRECT_URI,
        "grant_type": "authorization_code"
    }

    async with httpx.AsyncClient() as client:
        token_resp = await client.post(TOKEN_URI, data=data)
        token_data = token_resp.json()

        if "access_token" not in token_data:
            return HTMLResponse("Failed to get access token.", status_code=400)

        headers = {"Authorization": f"Bearer {token_data['access_token']}"}
        userinfo_resp = await client.get(USERINFO_URI, headers=headers)
        user_info = userinfo_resp.json()

    user_id = user_info.get("id")
    email = user_info.get("email")
    name = user_info.get("name")
    picture = user_info.get("picture")

    # Check if user exists
    existing_user = await database.fetch_one(
        select(users).where(users.c.id == user_id)
    )

    if existing_user:
        # Update last login timestamp
        await database.execute(
            update(users)
            .where(users.c.id == user_id)
            .values(last_login_at=func.now())
        )

        return HTMLResponse(
            content="""
                <script>
                    alert("Welcome back!");
                    window.location.href = "/";
                </script>
            """,
            status_code=200
        )

    # Insert new user
    await database.execute(
        insert(users).values(
            id=user_id,
            email=email,
            name=name,
            picture=picture,
            last_login_at=func.now()
        )
    )

    # Create credit wallet with 0 balance
    await database.execute(
        insert(user_credits).values(
            user_id=user_id,
            credits_balance=0
        )
    )

    return HTMLResponse(
        content=f"""
            <h3>Welcome, {name}!</h3>
            <img src="{picture}" width="100">
            <p>You have successfully signed in and a credit wallet has been created.</p>
        """,
        status_code=200
    )
