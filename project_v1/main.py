from fastapi import FastAPI
from auth.oauth_google import router as auth_router
from credits.credit_simulator import router as credit_router
from features.features_api import router as feature_router

from fastapi.responses import RedirectResponse, HTMLResponse

app = FastAPI()

# Register routes
app.include_router(auth_router, prefix="/auth")
app.include_router(credit_router, prefix="/credits")
app.include_router(feature_router, prefix="/features")
# app.include_router(feature_router)



from database.database import database


@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get("/")
async def homepage():
    return HTMLResponse('<a href="/auth/login">Login with Google</a>')
