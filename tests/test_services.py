from app.services import AdvantageEventService


def test_payment_service_create(db):
    from app.services import PaymentService
    from app.schemas import PaymentCreate

    service = PaymentService(db)

    data = PaymentCreate(
        clid="test",
        payout=100.0,
        ts="2024-01-01T10:00:00"
    )

    payment, created = service.get_or_create(data)

    assert created is True
    assert payment.clid == "test"


def test_advantage_event_created(db, click, payment):
    service = AdvantageEventService(db)

    event = service.get_or_create(click, payment)

    assert event.id is not None
    assert event.click_id == click.id
    assert event.payment_id == payment.id
