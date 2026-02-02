import os
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from supabase import create_client
from dotenv import load_dotenv
import uvicorn

load_dotenv()  

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")

if not SUPABASE_URL or not SUPABASE_ANON_KEY:
    raise RuntimeError("Supabase env vars not loaded")

supabase = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


class LoginData(BaseModel):
    email: str
    username: str
    password: str


@app.post("/api/login")
async def login(data: LoginData):
    email = data.email
    username = data.username
    password = data.password

    if len(password) < 6:
        return {"error": "Password must be at least 6 characters"}

    try:
        result = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })
        if result.user:
            return {
                "status": "logged_in",
                "user_id": result.user.id,
                "email": result.user.email,
                "display_name": result.user.user_metadata.get("display_name")
            }
    except Exception as login_error:
        print("LOGIN ERROR:", login_error)

    try:
        result = supabase.auth.sign_up({
            "email": email,
            "password": password,
            "options": {
                "data": {"display_name": username}
            }
        })
        if result.user:
            return {
                "status": "signed_up",
                "user_id": result.user.id,
                "email": result.user.email,
                "display_name": result.user.user_metadata.get("display_name")
            }
        return {"error": "Signup returned no user"}
    except Exception as signup_error:
        print("SIGNUP ERROR:", signup_error)
        return {"error": str(signup_error)}


@app.get("/", response_class=HTMLResponse)
async def serve_home():
    return templates.TemplateResponse("index.html", {"request": {}})

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8080)
