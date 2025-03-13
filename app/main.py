from fastapi import FastAPI
from app.api.v1.endpoints import ingest, insights, ai_insights

app = FastAPI()

# Incluir los routers
app.include_router(ingest.router)
app.include_router(insights.router)
app.include_router(ai_insights.router)