from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class PasteBase(BaseModel):
    paste_contents: str
    expires_at: Optional[int] = None

class PasteCreate(PasteBase):
    pass

class PasteRetrieve(PasteBase):
    created_at: datetime
