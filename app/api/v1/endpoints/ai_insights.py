from fastapi import APIRouter, HTTPException, Request
import logging
import pandas as pd
from app.services.ai_processing import calc_ai_insights
from app.core.logging import setup_logging
from typing import Dict

router = APIRouter()

setup_logging()

@router.get("/companies/{company_id}/ai-insights")
async def get_ai_insights(
    request: Request,
    company_id: str
) -> Dict[str, Dict]:
    # Verify if the data was loaded
    if not hasattr(request.app.state, 'datos') or request.app.state.datos.empty:
        logging.warning("No data available. Please ingest tweets first.")
        raise HTTPException(status_code=400, detail="No data available. Please ingest tweets first.")
    
    datos = request.app.state.datos
    
    try:
        insights = calc_ai_insights(datos, company_id)
        return insights
    except Exception as e:
        logging.error(f"Error generating AI insights: {e}")
        raise HTTPException(status_code=500, detail=f"Error generating AI insights: {e}")