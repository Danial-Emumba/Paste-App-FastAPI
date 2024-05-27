from operator import and_
from sqlalchemy.orm import Session
from app.db.models.paste import Paste
from datetime import datetime
from fastapi.exceptions import HTTPException

from app.db.models.user import User

def create_paste(db: Session, shortlink: str, expires_at: int):
    try:
        db_paste = Paste(shortlink=shortlink, expires_at=expires_at, created_at=datetime.now())
        db.add(db_paste)
        db.commit()
        db.refresh(db_paste)
    except Exception as e:
        print(f"Failed to create paste: {e}")

def get_paste_by_shortlink(db: Session, shortlink: str):
    try:
        paste = db.query(Paste).filter(Paste.shortlink == shortlink).first()
        if paste.expired:
            raise HTTPException(status_code=404, detail="This paste is expired.")
        return paste
    except Exception as e:
        print(f"Failed to get paste by shortlink: {e}")

def delete_expired_pastes(db: Session):
    try:
        current_time = datetime.now()
        expired_pastes = db.query(Paste).filter(and_(Paste.expires_at < current_time, Paste.expired != True)).all()
        print(f"Expired_pastes: {expired_pastes}")
        if not expired_pastes:
            print("No expired pastes found.")
            return

        print(f"Found {len(expired_pastes)} expired pastes to delete.")
        for paste in expired_pastes:
            print(f"Updating paste with id {paste.id} to expired=True.")
            paste.expired = True
        db.commit()
        print("Expired pastes successfully marked as expired.")
        return expired_pastes
    except Exception as e:
        print(f"Failed to delete expired pastes: {e}")

def delete_paste(db: Session, shortlink: str):
    try:
        db_paste = get_paste_by_shortlink(db, shortlink)
        if db_paste:
            db.delete(db_paste)
            db.commit()
            return True
        return False
    except Exception as e:
        print(f"Failed to delete paste: {e}")

def get_user_by_username(db: Session, username: str):
    try:
        user = db.query(User).filter(User.username == username).first()
        return user
    except Exception as e:
        print(f"Failed to get user by username: {e}")
        
def create_user(db: Session, username: str, password: str):
    try:
        db_user = User(username=username, password=password)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except Exception as e:
        print(f"Failed to create user: {e}")