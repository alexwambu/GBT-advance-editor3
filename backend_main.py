from fastapi import FastAPI, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import shutil
from backend_deploy_logic import handle_deployment

app = FastAPI()

# CORS config
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files (uploaded logos)
app.mount("/static", StaticFiles(directory="."), name="static")

@app.post("/deploy/")
async def deploy_app(
    repo_url: str = Form(...),
    domain: str = Form(...),
    logo: UploadFile = None
):
    logo_path = "frontend_logo.png"
    if logo:
        with open(logo_path, "wb") as f:
            shutil.copyfileobj(logo.file, f)

    return handle_deployment(repo_url, domain)
