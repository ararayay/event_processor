from app.clients import AdVantageClient
from app.models import AdvantageEvent
from app.models.advantage_event import EventStatus
from app.utils import logger


class AdvantageSenderService:
    """Сервис для отправки данных в AdVantage"""
    def __init__(self, db, client: AdVantageClient):
        self.db = db
        self.client = client

    def send(self, event: AdvantageEvent) -> bool:
        """Отправляет данные в AdVantage"""
        try:
            response = self.client.send_click(payload=event.payload)
            if response.is_success:
                logger.info("Sent request to AdVantage", extra={
                    "event_id": event.id,
                })
                event.status = EventStatus.sent
            else:
                logger.error("AdVantage event request failed", extra={
                    "error": response.text,
                    "event_id": event.id,
                })
                event.status = EventStatus.failed
                event.attempts += 1

            self.db.commit()
            return response.is_success

        except Exception as e:
            logger.error("AdVantage request failed", extra={
                "error": str(e),
                "event_id": event.id,
            })
            event.status = EventStatus.failed
            event.attempts += 1
            self.db.commit()
            return False
