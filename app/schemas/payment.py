from datetime import datetime

from pydantic import BaseModel


class PaymentCreate(BaseModel):
    """Схема для создания покупок"""
    clid: str
    payout: float
    ts: datetime
