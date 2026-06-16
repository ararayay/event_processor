from fastapi import APIRouter, Depends, status, HTTPException

from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas import PaymentCreate
from app.services import AdvantageEventService, ClickService, PaymentService

router = APIRouter(tags=["Payments"])

@router.post("/payment", status_code=status.HTTP_201_CREATED)
def create_payment(data: PaymentCreate, db: Session = Depends(get_db)):
    """Создание покупки"""
    payment, created = PaymentService(db).get_or_create(data)
    if not created:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Payment already exists")

    click = ClickService(db).get_by_clid(payment.clid)
    if click:
        AdvantageEventService(db).get_or_create(click, payment)

    return {"data": payment.id, "status": "ok"}
