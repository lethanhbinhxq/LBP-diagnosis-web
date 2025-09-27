# main.py
from fastapi import FastAPI
from core.config import configure_cors
from api import all_routers
from core.create_db import init_db  # Import the function

# Initialize DB at startup
init_db()

app = FastAPI()
configure_cors(app)

# Register all routers
for router in all_routers:
    app.include_router(router)
