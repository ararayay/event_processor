from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import AdvantageEvent, Payment, Click
from app.models.advantage_event import AdvantageEventPayload


class AdvantageEventService:
    """Сервис для работы с AdvantageEvent"""
    DEFAULT_CURRENCY = "USD"

    def __init__(self, db: Session):
        self.db = db

    def build_payload(self, click: Click, payment: Payment) -> AdvantageEventPayload:
        """Возвращает payload для отправки в AdvantageEvent"""
        return {
            "clid":         click.clid,
            "payout":       payment.payout,
            "click_spend":  click.click_spend,
            "click_ts":     click.ts.isoformat(),
            "payment_ts":   payment.ts.isoformat(),
            "payout_currency":      self.DEFAULT_CURRENCY,
            "click_spend_currency": self.DEFAULT_CURRENCY,
        }

    def get(self, click: Click, payment: Payment) -> AdvantageEvent | None:
        """Проверяет, существует ли AdvantageEvent по клику и покупке"""
        statement = select(AdvantageEvent).where(
            AdvantageEvent.click_id == click.id,
            AdvantageEvent.payment_id == payment.id,
        )

        return self.db.execute(statement).scalar_one_or_none()

    def create(self, click: Click, payment: Payment) -> AdvantageEvent:
        """Создаёт AdvantageEvent"""
        advantage_event = AdvantageEvent(
            payload=self.build_payload(click, payment),
            click_id=click.id,
            payment_id=payment.id
        )
        self.db.add(advantage_event)
        self.db.commit()
        self.db.refresh(advantage_event)
        return advantage_event

    def get_or_create(self, click: Click, payment: Payment) -> AdvantageEvent:
        """Создание события"""
        existing = self.get(click, payment)
        if existing:
            return existing
        return self.create(click, payment)
