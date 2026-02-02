import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from supabase import create_client
import os
from dotenv import load_dotenv
load_dotenv()
app = FastAPI()
supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_ANON_KEY")
)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

class LoginData(BaseModel):
    username: str
    password: str

@app.post("/api/login")
async def login(data: LoginData):
    email = data.username
    password = data.password

    try:
        result = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })

        if result.user:
            return {
                "status": "logged_in",
                "user_id": result.user.id,
                "email": result.user.email
            }

    except Exception as login_error:
        print("LOGIN ERROR:", login_error)

    try:
        result = supabase.auth.sign_up({
            "email": email,
            "password": password
        })

        if result.user:
            return {
                "status": "signed_up",
                "user_id": result.user.id,
                "email": result.user.email
            }

        return {"error": "Signup failed"}

    except Exception as signup_error:
        print("SIGNUP ERROR:", signup_error)
        return {
            "error": str(signup_error)
        }


@app.get("/", response_class=HTMLResponse)
async def serve_home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8080)
