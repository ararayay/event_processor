from fastapi import APIRouter, Depends, status

from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.payment import PaymentCreate
from app.services.advantage_event import AdvantageEventService
from app.services.click import ClickService
from app.services.payment import PaymentService

router = APIRouter(tags=["Payments"])

@router.post("/payment", status_code=status.HTTP_201_CREATED)
def create_payment(data: PaymentCreate, db: Session = Depends(get_db)):
    """Создание покупки"""
    payment, created = PaymentService(db).get_or_create(data)
    if not created:
        return {"message": "Payment already exists"}

    click = ClickService(db).get(payment.clid)
    if click:
        AdvantageEventService(db).get_or_create(click, payment)

    return {"data": payment.id, "status": "ok"}
