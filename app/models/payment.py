from sqlalchemy import String, Integer, Float, DateTime, func, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class Payment(Base):
    """Модель для хранения данных по покупкам"""
    __tablename__ = "payments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    clid: Mapped[str] = mapped_column(String, index=True, nullable=False)
    payout: Mapped[float] = mapped_column(Float, nullable=False)
    ts: Mapped[DateTime] = mapped_column(DateTime, nullable=False)

    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now(), nullable=False)

    __table_args__ = (UniqueConstraint("clid", "ts", name="unique_clid_ts"),)
