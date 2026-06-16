from fastapi import APIRouter, Depends, status

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
        return {"message": "Click already exists"}

    payments = PaymentService(db).get_all(click.clid)
    for payment in payments:
        AdvantageEventService(db).get_or_create(click, payment)

    return {"click_id": click.id, "status": "ok"}
