from fastapi import FastAPI

from app.api.click import router as click_router
from app.api.payment import router as payment_router

app = FastAPI()

app.include_router(click_router)
app.include_router(payment_router)