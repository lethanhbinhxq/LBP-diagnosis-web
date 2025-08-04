from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import router
from core.config import configure_cors

app = FastAPI()
configure_cors(app)

app.include_router(router)