# main.py
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from core.config import configure_cors, UPLOAD_DIR
from api import all_routers
from core.create_db import init_db  # Import the function

# Initialize DB at startup
init_db()

app = FastAPI()
configure_cors(app)

# Register all routers
for router in all_routers:
    app.include_router(router)

app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")