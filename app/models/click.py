from datetime import datetime

from sqlalchemy import String, Integer, Float, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class Click(Base):
    """Модель для хранения данных по кликам"""
    __tablename__ = "clicks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    clid: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    ad_id: Mapped[int] = mapped_column(Integer, nullable=False)
    click_spend: Mapped[float] = mapped_column(Float, nullable=False)
    ts: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)
