from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.config import configure_cors
from api import all_routers  # Import from __init__.py in /api

app = FastAPI()
configure_cors(app)

# Register all routers
for router in all_routers:
    app.include_router(router)
