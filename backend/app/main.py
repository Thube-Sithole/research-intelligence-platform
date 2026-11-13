from fastapi import FastAPI
from app.api.routes import router
from app.core.config import settings

app = FastAPI(title=settings.app_name, version="0.1.0")
app.include_router(router, prefix=settings.api_v1_prefix)


@app.get("/health")
async def health():
    return {"status": "ok", "environment": settings.app_env}
