def test_post_socio_exito_y_limpieza_email(client):
    body = {
        "nombre": " Socio Pytest ",
        "email": "SOCIO.PYTEST@CLUB.COM",
    }

    response = client.post("/socios", json=body)

    assert response.status_code == 201

    data = response.get_json()

    assert data["nombre"] == "Socio Pytest"
    assert data["email"] == "socio.pytest@club.com"
    assert data["activo"] is True

def test_post_socio_email_invalido_devuelve_400(client):
    body = {
        "nombre": "Socio Email Invalido",
        "email": "email_sin_formato_valido",
    }

    response = client.post("/socios", json=body)

    assert response.status_code == 400

    data = response.get_json()

    assert "errors" in data
    assert len(data["errors"]) > 0
    assert data["errors"][0]["code"] == "BAD_REQUEST"

def test_post_socio_email_duplicado_devuelve_409(client):
    body = {
        "nombre": "Socio Duplicado",
        "email": "duplicado.pytest@club.com",
    }

    client.post("/socios", json=body)

    response = client.post("/socios", json=body)

    assert response.status_code == 409