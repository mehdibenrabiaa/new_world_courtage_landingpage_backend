from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, JSON, DateTime
from core.database import Base


class Lead(Base):
    __tablename__ = "leads"

    id = Column(Integer, primary_key=True, index=True)
    lead_uid = Column(String, unique=True, index=True, nullable=True)
    status = Column(String, nullable=False, default="partial")
    name = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    insurance_type = Column(String, nullable=True)
    answers = Column(JSON, nullable=False, default=dict)
    source_path = Column(String, nullable=False)
    referrer = Column(String, nullable=True)
    user_agent = Column(String, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
