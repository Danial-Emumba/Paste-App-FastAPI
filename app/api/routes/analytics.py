from fastapi import APIRouter, HTTPException
from datetime import datetime
from app.services.analytics_service import get_monthly_visit_stats

router = APIRouter()


@router.get("/analytics/monthly")
def monthly_visit_stats():
    try:
        current_month = datetime.now().strftime("%Y-%m")
        return get_monthly_visit_stats(current_month)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve monthly visit stats: {e}")