import os

from sqlalchemy.orm import Session
from dotenv import load_dotenv

from app.clients import AdVantageClient
from app.services import AdvantageEventService, AdvantageSenderService
from app.db.session import SessionLocal


class AdvantageWorker:
    """Worker для отправки событий в AdVantage"""
    def __init__(self, db: Session, client: AdVantageClient):
        self.db = db
        self.client = client

    def run(self) -> None:
        """Запускает процесс отправки накопленных AdvantageEvent"""
        events = AdvantageEventService(self.db).get_unsent_events()
        sender = AdvantageSenderService(self.db, self.client)

        for event in events:
            sender.send(event)


def main():
    load_dotenv()
    db = SessionLocal()

    token = os.getenv("ADVANTAGE_TOKEN")
    base_url = os.getenv("ADVANTAGE_URL")

    if not token:
        raise ValueError("ADVANTAGE_TOKEN is not set")

    if not base_url:
        raise ValueError("ADVANTAGE_URL is not set")

    try:
        client = AdVantageClient(token, base_url)

        worker = AdvantageWorker(db, client)
        worker.run()
    finally:
        db.close()


if __name__ == "__main__":
    main()
