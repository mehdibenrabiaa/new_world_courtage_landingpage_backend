from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from sqlalchemy.orm.attributes import flag_modified

from core.database import get_db
from core.security import require_api_key
from models.lead import Lead
from models.schemas import LeadIn, LeadOut

router = APIRouter(prefix="/leads", tags=["leads"])


@router.post("", response_model=LeadOut, status_code=201)
def create_or_update_lead(payload: LeadIn, request: Request, db: Session = Depends(get_db)):
    # Upsert by lead_uid: the first call (as soon as name+phone are known)
    # creates a "partial" row; the final submit reuses the same lead_uid to
    # fill in the rest instead of creating a second row. The *current* row
    # still reflects the latest submission (so existing reads don't change),
    # but every submission is also appended to `history` first — nothing a
    # later submission overwrites is ever actually lost.
    lead = db.query(Lead).filter(Lead.lead_uid == payload.lead_uid).first()
    if not lead:
        lead = Lead(lead_uid=payload.lead_uid, history=[])
        db.add(lead)

    lead.history = [
        *(lead.history or []),
        {
            "at": datetime.now(timezone.utc).isoformat(),
            "name": payload.name,
            "phone": payload.phone,
            "insurance_type": payload.insurance_type,
            "answers": payload.answers,
            "completed": payload.completed,
        },
    ]
    flag_modified(lead, "history")  # JSON columns need an explicit nudge — mutating in place isn't auto-detected

    lead.name = payload.name
    lead.phone = payload.phone
    if payload.insurance_type:
        lead.insurance_type = payload.insurance_type
    lead.answers = payload.answers
    lead.source_path = payload.source_path
    lead.referrer = payload.referrer
    lead.user_agent = request.headers.get("user-agent")
    lead.status = "completed" if payload.completed else "partial"

    db.commit()
    db.refresh(lead)
    return lead


@router.get("", response_model=list[LeadOut], dependencies=[Depends(require_api_key)])
def list_leads(limit: int = 50, offset: int = 0, db: Session = Depends(get_db)):
    return (
        db.query(Lead)
        .order_by(Lead.created_at.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )


@router.get("/{lead_id}", response_model=LeadOut, dependencies=[Depends(require_api_key)])
def get_lead(lead_id: int, db: Session = Depends(get_db)):
    lead = db.query(Lead).filter(Lead.id == lead_id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    return lead
