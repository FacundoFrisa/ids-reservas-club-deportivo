def test_get_canchas_paginado_y_hateoas(client, sample_cancha):
    # 'sample_cancha' inserta una cancha previa para garantizar
    # que retorne 200 OK con datos.
    response = client.get("/canchas?_limit=2&_offset=0")

    assert response.status_code == 200

    data = response.get_json()

    assert "canchas" in data
    assert len(data["canchas"]) >= 1
    assert "_links" in data


def test_post_cancha_exito(client):
    body = {
        "nombre": "Cancha Test Pytest",
        "id_deporte": 1,
        "precio_hora": 1200000,
        "techada": True,
    }

    response = client.post("/canchas", json=body)

    assert response.status_code == 201

    data = response.get_json()

    assert data is not None, (
        "El endpoint POST /canchas debe devolver "
        "el objeto JSON creado"
    )
    assert data["nombre"] == "Cancha Test Pytest"
    assert data["techada"] is True


def test_post_cancha_precio_invalido_devuelve_400(client):
    body = {
        "nombre": "Cancha Gratis",
        "id_deporte": 1,
        "precio_hora": 0,
    }

    response = client.post("/canchas", json=body)

    assert response.status_code == 400

    data = response.get_json()

    assert "errors" in data
    assert len(data["errors"]) > 0
    assert data["errors"][0]["code"] == "BAD_REQUEST"


def test_get_cancha_por_id_inexistente_devuelve_404(client):
    response = client.get("/canchas/99999")

    assert response.status_code == 404