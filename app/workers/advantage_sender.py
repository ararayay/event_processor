import os
import time

from sqlalchemy.orm import Session
from dotenv import load_dotenv

from app.clients import AdVantageClient
from app.services import AdvantageEventService, AdvantageSenderService
from app.db.session import SessionLocal
from app.utils import logger


class AdvantageWorker:
    """Worker для отправки событий в AdVantage"""
    def __init__(self, db: Session, client: AdVantageClient):
        self.db = db
        self.client = client

    def run(self) -> None:
        """Запускает процесс отправки накопленных AdvantageEvent"""
        events = AdvantageEventService(self.db).get_unsent_events()
        sender = AdvantageSenderService(self.db, self.client)

        logger.info("Found %s unsent events", len(events))

        for event in events:
            sender.send(event)


def main():
    load_dotenv()

    token = os.getenv("ADVANTAGE_TOKEN")
    base_url = os.getenv("ADVANTAGE_URL")

    if not token:
        raise ValueError("ADVANTAGE_TOKEN is not set")

    if not base_url:
        raise ValueError("ADVANTAGE_URL is not set")

    client = AdVantageClient(token, base_url)

    interval_seconds = 300
    try:
        while True:
            db = SessionLocal()
            worker = AdvantageWorker(db, client)
            logger.info("Starting worker iteration")

            try:
                worker.run()
            except Exception:
                logger.exception("Worker iteration failed")

            logger.info("Sleeping for %s seconds", interval_seconds)
            time.sleep(interval_seconds)

    finally:
        db.close()


if __name__ == "__main__":
    main()
