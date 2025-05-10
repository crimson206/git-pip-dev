import sys

from datetime import datetime
from fastapi import FastAPI
from fastapi.responses import RedirectResponse, JSONResponse
import httpx
import os
from cryptography.fernet import Fernet
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# 환경변수에서 정보 로드
CLIENT_ID = os.getenv("GITHUB_CLIENT_ID")
CLIENT_SECRET = os.getenv("GITHUB_CLIENT_SECRET")
FERNET_KEY = os.getenv("FERNET_KEY")  # 32-byte base64-encoded key

fernet = Fernet(FERNET_KEY)

# 토큰 저장 파일 (간단한 파일 저장 예시, 실전은 DB 권장)
TOKEN_FILE = Path("token.enc")


@app.get("/login/github")
def login():
    return RedirectResponse(
        f"https://github.com/login/oauth/authorize"
        f"?client_id={CLIENT_ID}"
        f"&redirect_uri=http://localhost:8000/auth/github/callback"
        f"&scope=repo"
    )


@app.get("/logout")
def logout():
    if TOKEN_FILE.exists():
        TOKEN_FILE.unlink()
    return {"message": "Logged out successfully"}


@app.get("/status")
def login_status():
    if not TOKEN_FILE.exists():
        return {"logged_in": False, "message": "No token found."}

    try:
        encrypted = TOKEN_FILE.read_bytes()
        _ = fernet.decrypt(encrypted)
        created = datetime.fromtimestamp(TOKEN_FILE.stat().st_mtime)
        return {
            "logged_in": True,
            "last_token_update": created.isoformat(),
        }
    except Exception as e:
        return {"logged_in": False, "error": str(e)}


@app.get("/auth/github/callback")
async def github_callback(code: str):
    async with httpx.AsyncClient() as client:
        # 1. access token 요청
        token_resp = await client.post(
            "https://github.com/login/oauth/access_token",
            headers={"Accept": "application/json"},
            json={
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
                "code": code,
            },
        )
        token_json = token_resp.json()
        access_token = token_json.get("access_token")
        if not access_token:
            return JSONResponse({"error": "No access token received"}, status_code=400)

        # 2. access token 암호화 & 저장
        encrypted = fernet.encrypt(access_token.encode())
        TOKEN_FILE.write_bytes(encrypted)

        # 3. 유저 정보 요청
        user_resp = await client.get(
            "https://api.github.com/user",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        user_info = user_resp.json()

        return {
            "message": "Login successful. Access token encrypted and saved.",
            "user": user_info,
        }


@app.get("/use-token")
async def use_token():
    if not TOKEN_FILE.exists():
        return JSONResponse({"error": "No stored token"}, status_code=404)

    # 4. 복호화된 token 사용 예시 (리포 생성 등)
    encrypted = TOKEN_FILE.read_bytes()
    access_token = fernet.decrypt(encrypted).decode()

    async with httpx.AsyncClient() as client:
        repo_resp = await client.post(
            "https://api.github.com/user/repos",
            headers={
                "Authorization": f"Bearer {access_token}",
                "Accept": "application/vnd.github+json",
            },
            json={
                "name": "my-new-repo-from-fastapi",
                "private": False,
                "description": "Created via encrypted token",
            },
        )
        return repo_resp.json()
