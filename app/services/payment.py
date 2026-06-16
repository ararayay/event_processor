from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Payment
from app.schemas.payment import PaymentCreate


class PaymentService:
    """Сервис для работы с покупками"""
    def __init__(self, db: Session):
        self.db = db

    def get_by_clid_and_ts(self, data: PaymentCreate) -> Payment | None:
        """Возвращает покупку"""
        statement = select(Payment).where(
            Payment.clid == data.clid,
            Payment.ts == data.ts,
        )

        return self.db.execute(statement).scalar_one_or_none()

    def get_all(self, clid: str) -> Sequence[Payment]:
        """Возвращает все покупки по clid"""
        statement = select(Payment).where(
            Payment.clid == clid,
        )

        return self.db.execute(statement).scalars().all()

    def create(self, data: PaymentCreate) -> Payment:
        """Создаёт покупку"""
        payment = Payment(
            clid=data.clid,
            payout=data.payout,
            ts=data.ts,
        )
        self.db.add(payment)
        self.db.commit()
        self.db.refresh(payment)
        return payment

    def get_or_create(self, data: PaymentCreate) -> tuple[Payment, bool]:
        """Возвращает покупку и флаг, была ли она создана"""
        existing = self.get_by_clid_and_ts(data)
        if existing:
            return existing, False
        return self.create(data), True
