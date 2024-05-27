import redis
import os
from app.config.settings import Settings

settings = Settings()
redis_host = settings.REDIS_HOST
redis_port = settings.REDIS_PORT

redis_client = redis.StrictRedis(host=redis_host, port=redis_port, db=0)