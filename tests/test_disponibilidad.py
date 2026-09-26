def test_get_canchas_disponibles_exito(client):
    url = (
        "/canchas/disponibles"
        "?fecha=2026-10-15&hora_inicio=18:00:00&hora_fin=20:00:00"
    )

    response = client.get(url)

    assert response.status_code == 200

    data = response.get_json()

    assert "canchas" in data


def test_get_canchas_disponibles_horario_fuera_de_club_devuelve_400(client):
    # Horario antes de las 08:00 hs
    url = (
        "/canchas/disponibles"
        "?fecha=2026-10-15&hora_inicio=06:00:00&hora_fin=08:00:00"
    )

    response = client.get(url)

    assert response.status_code == 400