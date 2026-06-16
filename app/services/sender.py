from app.clients.advantage import AdVantageClient
from app.models import AdvantageEvent
from app.models.advantage_event import EventStatus

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
                event.status = EventStatus.sent
            else:
                event.status = EventStatus.failed
                event.attempts += 1

            self.db.commit()
            return response.is_success

        except Exception:
            event.status = EventStatus.failed
            event.attempts += 1
            self.db.commit()
            return False
