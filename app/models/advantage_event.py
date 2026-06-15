from sqlalchemy import Integer, DateTime, JSON, Enum, func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
import enum

from app.models.base import Base


class EventStatus(str, enum.Enum):
    pending = "pending"
    sent = "sent"
    failed = "failed"


class AdvantageEvent(Base):
    """Модель для хранения информации об отправке данных в AdVantage"""
    __tablename__ = "advantage_events"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    payload: Mapped[dict] = mapped_column(JSON, nullable=False)

    click_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("clicks.id"), nullable=True)
    payment_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("payments.id"), nullable=True)

    status: Mapped[EventStatus] = mapped_column(Enum(EventStatus), default=EventStatus.pending, nullable=False)
    attempts: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now(), nullable=False)
    updated_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
