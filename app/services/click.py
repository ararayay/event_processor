from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Click
from app.schemas.click import ClickCreate


class ClickService:
    """Сервис для работы с кликами"""
    def __init__(self, db: Session):
        self.db = db

    def get_by_clid(self, clid: str) -> Click | None:
        """Возвращает клик по clid"""
        statement = select(Click).where(
            Click.clid == clid,
        )

        return self.db.execute(statement).scalar_one_or_none()

    def create(self, data: ClickCreate) -> Click:
        """Создаёт клик"""
        click = Click(
            clid=data.clid,
            ad_id=data.ad_id,
            click_spend=data.click_spend,
            ts=data.ts,
        )
        self.db.add(click)
        self.db.commit()
        self.db.refresh(click)
        return click

    def get_or_create(self, data: ClickCreate) -> tuple[Click, bool]:
        """Возвращает клик и флаг, был ли он создан"""
        existing = self.get_by_clid(data.clid)
        if existing:
            return existing, False
        return self.create(data), True
