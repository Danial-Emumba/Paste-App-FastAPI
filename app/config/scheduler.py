from apscheduler.schedulers.background import BackgroundScheduler
from tasks.expired_pastes_job import cleanup_expired_pastes

scheduler = BackgroundScheduler()

def setup_scheduler():
    scheduler.add_job(id='cleanup_pastes_job', func=cleanup_expired_pastes, trigger='interval', minutes=2)
    scheduler.start()

def shutdown_scheduler():
    scheduler.shutdown(wait=False)
