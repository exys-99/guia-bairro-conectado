import pytest
from app import create_app


@pytest.fixture
def client():
    app = create_app({"TESTING": True, "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"})
    with app.test_client() as client:
        yield client


def test_cadastro_e_listagem(client):
    resp = client.post(
        "/api/estabelecimentos",
        json={
            "nome_negocio": "Marmitaria Sabor de Casa",
            "id_categoria": 1,
            "telefone_whatsapp": "86999990001",
            "ponto_referencia": "Próximo à Praça da Igreja",
            "horario_abertura": "08:00",
            "horario_fechamento": "14:30",
            "item_titulo": "Marmita Executiva",
            "item_preco": 16.0,
        },
    )
    assert resp.status_code == 201

    busca = client.get("/api/estabelecimentos?q=marmita")
    dados = busca.get_json()
    assert len(dados) == 1
    assert dados[0]["nome_negocio"] == "Marmitaria Sabor de Casa"
    assert "api.whatsapp.com/send?phone=5586999990001" in dados[0]["link_whatsapp"]


def test_bloqueio_whatsapp_invalido(client):
    resp = client.post(
        "/api/estabelecimentos",
        json={
            "nome_negocio": "Teste Inválido",
            "id_categoria": 1,
            "telefone_whatsapp": "9999",
            "ponto_referencia": "Rua A",
            "horario_abertura": "08:00",
            "horario_fechamento": "18:00",
        },
    )
    assert resp.status_code == 400