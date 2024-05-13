from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.api.models.paste import PasteCreate, PasteRetrieve
from app.db.setup import SessionLocal
from app.services.paste_service import generate_shortlink, save_paste_to_storage, get_paste_content_from_storage, create_paste, get_paste_service, delete_paste_service

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/paste/")
def create_paste_api(paste: PasteCreate, db: Session = Depends(get_db)):
    try:
        shortlink = generate_shortlink()    
        if paste.expires_at:
            expiration = datetime.now() + timedelta(minutes=paste.expires_at)
        else:
            expiration = None
        create_paste(db, shortlink, expiration)
        save_paste_to_storage(shortlink, paste.paste_contents)
        return {"shortlink": shortlink}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to create paste")

@router.get("/paste/", response_model=PasteRetrieve)
def retrieve_paste_api(shortlink: str, db: Session = Depends(get_db)):
    try:
        paste = get_paste_service(db, shortlink)
        if paste is None:
            raise HTTPException(status_code=404, detail="Paste not found")
        paste_contents = get_paste_content_from_storage(shortlink)
        if paste_contents is None:
            raise HTTPException(status_code=404, detail="Paste content not found in S3")
        expires_at = None
        if paste.expires_at:
            expires_at = (paste.expires_at - datetime.now()).total_seconds() / 60
        return {
            "paste_contents": paste_contents,
            "created_at": paste.created_at,
            "expires_at": expires_at
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to retrieve paste")

@router.delete("/paste/")
def delete_paste_api(shortlink: str, db: Session = Depends(get_db)):
    try:
        paste = get_paste_service(db, shortlink)
        if paste is None:
            raise HTTPException(status_code=404, detail="Paste not found")
        delete_paste_service(db, shortlink)
        return {"message": "Paste deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to delete paste")
