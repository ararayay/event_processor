from fastapi import APIRouter, Depends, status, HTTPException

from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.click import ClickCreate
from app.services.advantage_event import AdvantageEventService
from app.services.click import ClickService
from app.services.payment import PaymentService

router = APIRouter(tags=["Clicks"])

@router.post("/click", status_code=status.HTTP_201_CREATED)
def create_click(data: ClickCreate, db: Session = Depends(get_db)):
    """Создание клика"""
    click, created = ClickService(db).get_or_create(data)
    if not created:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Click already exists")

    payments = PaymentService(db).get_all_by_clid(click.clid)
    for payment in payments:
        AdvantageEventService(db).get_or_create(click, payment)

    return {"data": click.id, "status": "ok"}
