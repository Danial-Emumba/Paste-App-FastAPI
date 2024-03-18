from fastapi import FastAPI
from uvicorn import run
from app.db.setup import create_database
from app.api.routes import paste, analytics
from app.api.middlewares.exceptions import ExceptionHandlerMiddleware
from dotenv import load_dotenv, find_dotenv
from apscheduler.schedulers.background import BackgroundScheduler
import asyncio
from app.config.scheduler import setup_scheduler, shutdown_scheduler

_ = load_dotenv(find_dotenv())
scheduler = BackgroundScheduler()

def job_counter():
    counter = 0
    print('job_counter: ', counter)
    counter += 1

app = FastAPI()

async def startup():
    setup_scheduler()
    create_database()

async def shutdown():
    shutdown_scheduler()
    pass

app.add_event_handler("startup", startup)
app.add_event_handler("shutdown", shutdown)

app.add_middleware(ExceptionHandlerMiddleware)

app.include_router(paste.router)
app.include_router(analytics.router)

async def run_app():
        run("main:app", reload=True, port=8000, host="127.0.0.1")

if __name__ == '__main__':
    asyncio.run(run_app())