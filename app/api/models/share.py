from pydantic import BaseModel, EmailStr

class ShareCreate(BaseModel):
    """
    Schema for creating a new share.
    """
    paste_id: int
    email: EmailStr
    can_edit: bool = False

class ShareUpdate(BaseModel):
    """
    Schema for updating an existing share.
    """
    can_edit: bool = False
