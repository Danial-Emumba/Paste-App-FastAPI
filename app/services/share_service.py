from sqlalchemy.orm import Session
from app.db.models import Share
from app.api.models.share import ShareCreate

"""
This code snippet contains three functions related to managing shares in a database.

create_share:
    Creates a new share in the database using the provided ShareCreate object.
    Parameters:
        - db: SQLAlchemy Session object for database operations.
        - share: ShareCreate object containing the data for the new share.
    Returns:
        - The created Share object.

list_shares:
    Retrieves a list of shares from the database based on the provided paste_id.
    Parameters:
        - db: SQLAlchemy Session object for database operations.
        - paste_id: Integer representing the paste_id to filter shares.
    Returns:
        - List of Share objects matching the paste_id.

delete_share:
    Deletes a share from the database based on the provided id.
    Parameters:
        - db: SQLAlchemy Session object for database operations.
        - id: Integer representing the id of the share to delete.
    Returns:
        - The deleted Share object.
    Raises:
        - HTTPException with status_code 404 if the share is not found.
"""

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
