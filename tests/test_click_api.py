def test_create_click(client):
    response = client.post("/click", json={
        "clid": "test123",
        "ad_id": 1,
        "click_spend": 10.5,
        "ts": "2024-01-01T10:00:00"
    })

    assert response.status_code == 201
    assert response.json()["status"] == "ok"

def test_click_duplicate(client):
    payload = {
        "clid": "same_click",
        "ad_id": 1,
        "click_spend": 10.0,
        "ts": "2024-01-01T10:00:00"
    }

    r1 = client.post("/click", json=payload)
    r2 = client.post("/click", json=payload)

    assert r1.status_code == 201
    assert r2.status_code in (200, 409)
