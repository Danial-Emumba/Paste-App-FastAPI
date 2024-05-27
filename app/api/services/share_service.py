from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.db.models.share import Share
from app.api.models.share import ShareCreate, ShareUpdate
from app.api.utils.jwt import get_current_user_from_token

"""
This code snippet contains four functions related to managing shares in a database.

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

update_share:
    Updates an existing share in the database.
    Parameters:
        - db: SQLAlchemy Session object for database operations.
        - id: Integer representing the id of the share to update.
        - share_update: ShareUpdate object containing the updated data for the share.
    Returns:
        - The updated Share object.
    Raises:
        - HTTPException with status_code 404 if the share is not found.
"""

def create_share(db: Session, share: ShareCreate, current_user: User):
    """
    Creates a new share in the database for the current user.

    Args:
        db: SQLAlchemy Session object for database operations.
        share: ShareCreate object containing the data for the new share.
        current_user: The current user object.

    Returns:
        The created Share object.
    """
    db_share = Share(**share.dict(), created_by=current_user.id)
    db.add(db_share)
    db.commit()
    db.refresh(db_share)
    return db_share

def list_shares(db: Session, paste_id: int):
    return db.query(Share).filter(Share.paste_id == paste_id).all()

def delete_share(db: Session, id: int, current_user: User):
    """
    Deletes a share from the database for the current user.

    Args:
        db: SQLAlchemy Session object for database operations.
        id: Integer representing the id of the share to delete.
        current_user: The current user object.

    Returns:
        The deleted Share object.
    Raises:
        HTTPException with status_code 404 if the share is not found.
        HTTPException with status_code 403 if the current user is not the owner of the share.
    """
    db_share = db.query(Share).filter(Share.id == id).first()
    if db_share is None:
        raise HTTPException(status_code=404, detail="Share not found")
    if db_share.created_by != current_user.id:
        raise HTTPException(status_code=403, detail="You are not authorized to delete this share")
    db.delete(db_share)
    db.commit()
    return db_share

def update_share(db: Session, id: int, share_update: ShareUpdate, current_user: User):
    """
    Updates an existing share in the database for the current user.

    Args:
        db: SQLAlchemy Session object for database operations.
        id: Integer representing the id of the share to update.
        share_update: ShareUpdate object containing the updated data for the share.
        current_user: The current user object.

    Returns:
        The updated Share object.
    Raises:
        HTTPException with status_code 404 if the share is not found.
        HTTPException with status_code 403 if the current user is not the owner of the share.
    """
    db_share = db.query(Share).filter(Share.id == id).first()
    if db_share is None:
        raise HTTPException(status_code=404, detail="Share not found")
    if db_share.created_by != current_user.id:
        raise HTTPException(status_code=403, detail="You are not authorized to update this share")
    
    for key, value in share_update.dict().items():
        setattr(db_share, key, value)
    
    db.commit()
    db.refresh(db_share)
    return db_share
