from fastapi import APIRouter, HTTPException, Request
import logging
import pandas as pd
from app.services.data_processing import calc_response_rate, calc_conversation_ratio, calc_volume_metrics, calc_average_response_time
from app.core.logging import setup_logging
from typing import Dict

router = APIRouter()

setup_logging()

@router.get("/companies/{company_id}/insights")
async def get_company_insights(
    request: Request,
    company_id: str
) -> Dict[str, float]:
    # Verify if the data was loaded
    if not hasattr(request.app.state, 'datos') or request.app.state.datos.empty:
        logging.warning("No data available. Please ingest tweets first.")
        raise HTTPException(status_code=400, detail="No data available. Please ingest tweets first.")
    
    datos = request.app.state.datos
    
    logging.info(f"Fetching insights for company {company_id}.")
    
    # Calculate metrics
    response_rate = calc_response_rate(datos, company_id)
    conversation_ratio = calc_conversation_ratio(datos, company_id)
    volume_metrics = calc_volume_metrics(datos, company_id)
    average_minutes = calc_average_response_time(datos, company_id)

    insights = {
        "response_rate": response_rate,
        "conversation_ratio": conversation_ratio,
        "volume_metrics": volume_metrics,
        "average_response_time": average_minutes
    }
    
    logging.info(f"Insights successfully fetched for company {company_id}.")
    
    return insights