def test_read_main(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Bienvenido a USTA Trainer API"}

def test_get_exercises(client):
    # Prueba de éxito (200) cuando hay datos
    response = client.get("/api/v1/exercises")
    assert response.status_code == 200
    assert isinstance(response.json(), list)