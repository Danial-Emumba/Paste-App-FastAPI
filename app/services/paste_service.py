from datetime import datetime, timedelta
import secrets
from app.db.repository import create_paste, get_paste_by_shortlink, delete_paste
from app.storage.s3 import save_to_s3, get_paste_from_s3, delete_from_s3
from app.services.analytics_service import increment_visit_count

def generate_shortlink():
    return secrets.token_urlsafe(5)

def save_paste_to_storage(shortlink, paste_contents):
    try:
        save_to_s3(shortlink, paste_contents)
    except Exception as e:
        print(f"Failed to save paste to storage: {e}")

def get_paste_content_from_storage(shortlink):
    try:
        return get_paste_from_s3(shortlink)
    except Exception as e:
        print(f"Failed to get paste content from storage: {e}")

def get_paste_service(db, shortlink):
    try:
        increment_visit_count(shortlink)
        return get_paste_by_shortlink(db, shortlink)
    except Exception as e:
        print(f"Failed to get paste from database: {e}")

def create_paste_entry(shortlink, expires_at, paste_contents, db):
    try:
        expiration = None
        if expires_at:
            expiration = datetime.now() + timedelta(minutes=expires_at)
        
        create_paste(db, shortlink, expiration, datetime.now(), paste_contents)
    except Exception as e:
        print(f"Failed to create paste entry: {e}")

def delete_paste_service(db, shortlink):
    try:
        deleted = delete_paste(db, shortlink)
        if deleted:
            delete_from_s3(shortlink)
            return deleted
        return False
    except Exception as e:
        print(f"Failed to delete paste: {e}")
