def test_create_payment(client):
    response = client.post("/payment", json={
        "clid": "test123",
        "payout": 50.0,
        "ts": "2024-01-01T11:00:00"
    })

    assert response.status_code == 201
    assert response.json()["status"] == "ok"

def test_payment_duplicate(client):
    payload = {
        "clid": "same_payment",
        "payout": 50.0,
        "ts": "2024-01-01T11:00:00"
    }

    r1 = client.post("/payment", json=payload)
    r2 = client.post("/payment", json=payload)

    assert r1.status_code == 201
    assert r2.status_code in (200, 409)
