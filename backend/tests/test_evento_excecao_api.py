from datetime import datetime

from app.utils.auth import gerar_token


def test_criar_excecao_cancelamento_via_api(client, admin, evento_rec_segunda):
    token = gerar_token(admin.id, admin.tipo.name)
    payload = {
        'evento_recorrente_id': evento_rec_segunda.id,
        'data_original': '2025-01-06T10:00:00',
        'tipo': 'cancelamento',
        'motivo': 'Teste de cancelamento',
        'criado_por': admin.id,
    }

    response = client.post(
        '/eventos/excecoes',
        json=payload,
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == 201
    data = response.get_json()
    assert data['tipo'] == 'CANCELAMENTO'
    assert data['motivo'] == 'Teste de cancelamento'
    assert data['data_nova'] is None
    assert data['hora_nova_inicio'] is None
    assert data['hora_nova_fim'] is None
