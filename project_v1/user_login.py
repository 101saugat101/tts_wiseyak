import os
from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse, HTMLResponse
from urllib.parse import urlencode
import httpx
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, String, MetaData, Table, DateTime, func
import databases
from database.database import user_credits  # assuming your user_credits is defined there


# Load .env
load_dotenv()

# OAuth config
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")
AUTH_URI = os.getenv("AUTH_URI")
TOKEN_URI = os.getenv("TOKEN_URI")
USERINFO_URI = os.getenv("USERINFO_URI")

# Database config
DATABASE_URL = "postgresql://postgres:heheboii420@localhost/SAAS"
database = databases.Database(DATABASE_URL)
metadata = MetaData()

# Users table (updated)
users = Table(
    "users",
    metadata,
    Column("id", String, primary_key=True),  # Google OAuth ID
    Column("email", String, nullable=False),
    Column("name", String),
    Column("picture", String),
    Column("created_at", DateTime(timezone=True), server_default=func.now()),
    Column("last_login_at", DateTime(timezone=True))
)

# Create engine and table
engine = create_engine(DATABASE_URL)
metadata.create_all(engine)

# FastAPI app
app = FastAPI()


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get("/")
async def index():
    return HTMLResponse('<a href="/login">Login with Google</a>')


@app.get("/login")
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


# @app.get("/auth/callback")
# async def auth_callback(request: Request):
#     code = request.query_params.get("code")
#     if not code:
#         return HTMLResponse("No authorization code provided.", status_code=400)

#     # Exchange code for access token
#     data = {
#         "code": code,
#         "client_id": CLIENT_ID,
#         "client_secret": CLIENT_SECRET,
#         "redirect_uri": REDIRECT_URI,
#         "grant_type": "authorization_code"
#     }

#     async with httpx.AsyncClient() as client:
#         token_resp = await client.post(TOKEN_URI, data=data)
#         token_data = token_resp.json()

#         if "access_token" not in token_data:
#             return HTMLResponse("Failed to get token", status_code=400)

#         headers = {"Authorization": f"Bearer {token_data['access_token']}"}
#         userinfo_resp = await client.get(USERINFO_URI, headers=headers)
#         user_info = userinfo_resp.json()

#     user_id = user_info.get("id")

#     # Check if user already exists
#     query = users.select().where(users.c.id == user_id)
#     existing_user = await database.fetch_one(query)

#     if existing_user:
#         # Update last_login_at timestamp
#         update_query = users.update().where(users.c.id == user_id).values(
#             last_login_at=func.now()
#         )
#         await database.execute(update_query)

#         return HTMLResponse(
#             content=f"""
#                 <script>
#                     alert("Welcome back!");
#                     window.location.href = "/";
#                 </script>
#             """,
#             status_code=200
#         )

#     # Insert new user
#     insert_query = users.insert().values(
#         id=user_id,
#         email=user_info.get("email"),
#         name=user_info.get("name"),
#         picture=user_info.get("picture"),
#         last_login_at=func.now()
#     )
#     await database.execute(insert_query)

#     return HTMLResponse(
#         content=f"""
#             <h3>Welcome, {user_info.get("name")}!</h3>
#             <img src="{user_info.get("picture")}" width="100">
#             <p>You have successfully signed in.</p>
#         """,
#         status_code=200
#     )
@app.get("/auth/callback")
async def auth_callback(request: Request):
    code = request.query_params.get("code")
    if not code:
        return HTMLResponse("No authorization code provided.", status_code=400)

    # Exchange code for access token
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
            return HTMLResponse("Failed to get token", status_code=400)

        headers = {"Authorization": f"Bearer {token_data['access_token']}"}
        userinfo_resp = await client.get(USERINFO_URI, headers=headers)
        user_info = userinfo_resp.json()

    user_id = user_info.get("id")

    # Check if user already exists
    query = users.select().where(users.c.id == user_id)
    existing_user = await database.fetch_one(query)

    if existing_user:
        # Update last_login_at timestamp
        update_query = users.update().where(users.c.id == user_id).values(
            last_login_at=func.now()
        )
        await database.execute(update_query)

        return HTMLResponse(
            content=f"""
                <script>
                    alert("Welcome back!");
                    window.location.href = "/";
                </script>
            """,
            status_code=200
        )

    # Insert new user
    await database.execute(
        users.insert().values(
            id=user_id,
            email=user_info.get("email"),
            name=user_info.get("name"),
            picture=user_info.get("picture"),
            last_login_at=func.now()
        )
    )

    # Insert default credit wallet (🔥 important!)
    await database.execute(
        user_credits.insert().values(
            user_id=user_id,
            credits_balance=0
        )
    )

    return HTMLResponse(
        content=f"""
            <h3>Welcome, {user_info.get("name")}!</h3>
            <img src="{user_info.get("picture")}" width="100">
            <p>You have successfully signed in and a credit wallet has been created.</p>
        """,
        status_code=200
    )
