from fastapi import FastAPI
from src.api.routes import router

app = FastAPI(title="AI Email Response Agent")
app.include_router(router)