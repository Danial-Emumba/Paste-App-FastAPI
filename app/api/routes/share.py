from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services import share_service
from app.api.models.share import ShareCreate, ShareResponse

router = APIRouter()

@router.post('/share/', response_model=ShareResponse)
def create_share(share: ShareCreate, db: Session = Depends(get_db)):
    return share_service.create_share(db=db, share=share)

@router.get('/share/{paste_id}', response_model=List[ShareResponse])
def list_shares(paste_id: int, db: Session = Depends(get_db)):
    return share_service.list_shares(db=db, paste_id=paste_id)

@router.delete('/share/{id}', response_model=ShareResponse)
def delete_share(id: int, db: Session = Depends(get_db)):
    return share_service.delete_share(db=db, id=id)
