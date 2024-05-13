from fastapi import APIRouter
from datetime import datetime
from app.config.redis_client import redis_client

router = APIRouter()

def get_monthly_visit_stats(current_month):
    try:
        visit_counts = {}
        response = {}
        for key in redis_client.scan_iter(match=current_month + ":*"):
            shortlink = key.decode("utf-8").split(":")[1]
            visit_counts[shortlink] = int(redis_client.get(key))
        response = {current_month: visit_counts}
        return response
    except Exception as e:
        print(f"Failed to retrieve monthly visit stats: {e}")
        
def increment_visit_count(shortlink):
    try:
        key = f"{datetime.now().strftime('%Y-%m')}:{shortlink}"
        redis_client.incr(key)
    except Exception as e:
        print(f"Failed to increment visit count: {e}")