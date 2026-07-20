from pydantic import BaseModel
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session

from core.database import get_db
from core.security import require_api_key

router = APIRouter(prefix="/admin", tags=["admin"], dependencies=[Depends(require_api_key)])


class SqlQuery(BaseModel):
    query: str


@router.post("/sql")
def run_sql(payload: SqlQuery, db: Session = Depends(get_db)):
    query = payload.query.strip()
    if not query:
        raise HTTPException(status_code=400, detail="Query is required")

    try:
        result = db.execute(text(query))
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

    if result.returns_rows:
        columns = list(result.keys())
        rows = [list(row) for row in result.fetchall()]
        return {"columns": columns, "rows": rows, "row_count": len(rows)}
    return {"columns": [], "rows": [], "row_count": result.rowcount}
