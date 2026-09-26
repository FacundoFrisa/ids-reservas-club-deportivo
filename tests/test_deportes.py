def test_get_deportes_exito(client):
    response = client.get("/deportes")

    assert response.status_code == 200

    data = response.get_json()

    assert "deportes" in data
    assert isinstance(data["deportes"], list)
    assert len(data["deportes"]) >= 3