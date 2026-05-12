from datetime import date, datetime, timedelta
from typing import Optional

from app.models.evento_recorrente import EventoRecorrente


def gerar_ocorrencias(
    evento: EventoRecorrente,
    inicio: date,
    fim: date,
) -> list[dict]:
    """
    Dado um EventoRecorrente e um intervalo [inicio, fim],
    retorna a lista de ocorrências que caem nesse intervalo.

    Exemplo:
        evento.dia_semana = 6  (domingo)
        evento.hora_inicio = time(9, 0)
        inicio = date(2026, 5, 11)
        fim    = date(2026, 6, 11)

        → retorna 5 ocorrências (todos os domingos do intervalo)
    """
    if not evento.ativo:
        return []

    ocorrencias = []

    # Quantos dias faltam até o próximo dia_semana a partir de inicio
    # weekday() == 0 segunda ... 6 domingo — mesma convenção do nosso modelo
    dias_ate_primeiro = (evento.dia_semana - inicio.weekday()) % 7
    primeiro_dia = inicio + timedelta(days=dias_ate_primeiro)

    dia_atual = primeiro_dia
    while dia_atual <= fim:
        ocorrencias.append(_montar_ocorrencia(evento, dia_atual))
        dia_atual += timedelta(weeks=1)

    return ocorrencias


def _montar_ocorrencia(evento: EventoRecorrente, dia: date) -> dict:
    """Monta o dict de uma ocorrência individual."""
    hora_inicio = evento.hora_inicio
    hora_fim = evento.hora_fim

    return {
        'source_type': 'recorrente',
        'source_id': evento.id,
        'titulo': evento.titulo,
        'descricao': evento.descricao,
        'data_inicio': datetime.combine(dia, hora_inicio).isoformat(),
        'data_fim': datetime.combine(dia, hora_fim).isoformat() if hora_fim else None,
        'dia_semana': evento.dia_semana,
        'criado_por': evento.criado_por,
    }