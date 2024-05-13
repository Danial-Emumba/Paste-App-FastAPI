from sqlalchemy.orm import Session
from app.db.models import Share
from app.api.models.share import ShareCreate

def create_share(db: Session, share: ShareCreate):
    db_share = Share(**share.dict())
    db.add(db_share)
    db.commit()
    db.refresh(db_share)
    return db_share

def list_shares(db: Session, paste_id: int):
    return db.query(Share).filter(Share.paste_id == paste_id).all()

def delete_share(db: Session, id: int):
    db_share = db.query(Share).filter(Share.id == id).first()
    if db_share is None:
        raise HTTPException(status_code=404, detail="Share not found")
    db.delete(db_share)
    db.commit()
    return db_share
