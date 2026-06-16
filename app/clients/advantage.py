import httpx

from app.models.advantage_event import AdvantageEventPayload


class AdVantageClient:
    """Клиент для работы с AdVantage"""
    def __init__(self, token: str, base_url: str):
        self.token = token
        self.base_url = base_url

    def send_click(self, payload: AdvantageEventPayload) -> httpx.Response:
        return httpx.post(
            f"{self.base_url}/click",
            headers={"Authorization": f"Bearer {self.token}"},
            json=payload,
            timeout=10,
        )
