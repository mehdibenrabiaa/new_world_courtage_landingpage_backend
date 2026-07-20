from datetime import datetime
from pydantic import BaseModel


class LeadIn(BaseModel):
    lead_uid: str
    name: str
    phone: str
    insurance_type: str | None = None
    answers: dict = {}
    source_path: str
    referrer: str | None = None
    completed: bool = False


class LeadOut(BaseModel):
    id: int
    lead_uid: str | None
    status: str
    name: str
    phone: str
    insurance_type: str | None
    answers: dict
    history: list
    source_path: str
    referrer: str | None
    user_agent: str | None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
