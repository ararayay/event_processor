from datetime import datetime

from pydantic import BaseModel


class ClickCreate(BaseModel):
    """Схема для создания кликов"""
    clid: str
    ad_id: int
    click_spend: float
    ts: datetime
