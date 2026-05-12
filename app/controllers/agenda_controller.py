from datetime import date, datetime

from flask import Blueprint, jsonify, request

from app.models.evento_normal import EventoNormal, EventoStatus
from app.models.evento_recorrente import EventoRecorrente
from app.utils.recurrence import gerar_ocorrencias

agenda_bp = Blueprint('agenda', __name__)


def _parse_date(value: str, nome: str) -> date:
    try:
        return date.fromisoformat(value)
    except (ValueError, TypeError):
        raise ValueError(f"Formato de data inválido para '{nome}'. Use YYYY-MM-DD (ex: 2026-05-01)")


def _serialize_normal(evento: EventoNormal) -> dict:
    return {
        'source_type': 'normal',
        'source_id': evento.id,
        'titulo': evento.titulo,
        'descricao': evento.descricao,
        'data_inicio': evento.data_inicio.isoformat() if evento.data_inicio else None,
        'data_fim': evento.data_fim.isoformat() if evento.data_fim else None,
        'status': evento.status.value,
        'criado_por': evento.criado_por,
    }


@agenda_bp.route('/agenda', methods=['GET'])
def get_agenda():
    """
    Retorna todos os eventos (normais + ocorrências de recorrentes)
    dentro do intervalo informado.

    Query params:
        inicio  YYYY-MM-DD  obrigatório
        fim     YYYY-MM-DD  obrigatório

    Exemplo:
        GET /agenda?inicio=2026-05-01&fim=2026-05-31
    """
    inicio_str = request.args.get('inicio')
    fim_str = request.args.get('fim')

    if not inicio_str:
        return jsonify({'error': "'inicio' é obrigatório (YYYY-MM-DD)"}), 400
    if not fim_str:
        return jsonify({'error': "'fim' é obrigatório (YYYY-MM-DD)"}), 400

    try:
        inicio = _parse_date(inicio_str, 'inicio')
        fim = _parse_date(fim_str, 'fim')
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

    if fim < inicio:
        return jsonify({'error': "'fim' não pode ser anterior a 'inicio'"}), 400

    # Eventos normais no intervalo (ignora cancelados)
    eventos_normais = (
        EventoNormal.query
        .filter(
            EventoNormal.status == EventoStatus.ATIVO,
            EventoNormal.data_inicio >= datetime.combine(inicio, datetime.min.time()),
            EventoNormal.data_inicio <= datetime.combine(fim, datetime.max.time()),
        )
        .all()
    )

    # Ocorrências geradas dos eventos recorrentes ativos
    recorrentes = EventoRecorrente.query.filter_by(ativo=True).all()
    ocorrencias = []
    for evento in recorrentes:
        ocorrencias.extend(gerar_ocorrencias(evento, inicio, fim))

    # Unifica e ordena por data_inicio
    todos = [_serialize_normal(e) for e in eventos_normais] + ocorrencias
    todos.sort(key=lambda e: e['data_inicio'] or '')

    return jsonify(todos)
