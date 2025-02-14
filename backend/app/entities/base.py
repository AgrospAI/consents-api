from uuid import UUID
from pydantic import BaseModel
from datetime import datetime

class Base(BaseModel):
    uuid: UUID
    created_at: datetime
    is_active: bool = True
