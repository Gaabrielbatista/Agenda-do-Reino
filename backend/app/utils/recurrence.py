from datetime import date, datetime, timedelta

from app.models.evento_recorrente import EventoRecorrente
from app.models.evento_excecao import EventoExcecao, ExcecaoTipo


def gerar_ocorrencias(
    evento: EventoRecorrente,
    inicio: date,
    fim: date,
) -> list[dict]:
    """
    Dado um EventoRecorrente e um intervalo [inicio, fim],
    retorna a lista de ocorrências que caem nesse intervalo,
    aplicando automaticamente as exceções cadastradas.

    - CANCELAMENTO: a ocorrência é removida da lista.
    - REMARCACAO:   a ocorrência é substituída pela versão remarcada.
    """
    if not evento.ativo:
        return []
    
    # Evita N+1
    excecoes: dict[date, EventoExcecao] = {
        e.data_original.date(): e
        for e in EventoExcecao.query.filter_by(evento_recorrente_id=evento.id).all()
    }

    ocorrencias = []

    dias_ate_primeiro = (evento.dia_semana - inicio.weekday()) % 7
    primeiro_dia = inicio + timedelta(days=dias_ate_primeiro)

    dia_atual = primeiro_dia
    while dia_atual <= fim:
        excecao = excecoes.get(dia_atual)

        if excecao is None:
            # Ocorrência normal
            ocorrencias.append(_montar_ocorrencia(evento, dia_atual))

        elif excecao.tipo == ExcecaoTipo.REMARCACAO:
            # Substitui pela versão remarcada
            ocorrencias.append(_montar_ocorrencia_remarcada(evento, excecao))

        # CANCELAMENTO → simplesmente não adiciona

        dia_atual += timedelta(weeks=1)

    return ocorrencias


def _montar_ocorrencia(evento: EventoRecorrente, dia: date) -> dict:
    """Monta o dict de uma ocorrência normal."""
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
        'excecao_id': None,
    }


def _montar_ocorrencia_remarcada(evento: EventoRecorrente, excecao: EventoExcecao) -> dict:
    """Monta o dict de uma ocorrência remarcada."""
    # Data: usa data_nova se informada, senão mantém a data original
    if excecao.data_nova:
        data_base = excecao.data_nova.date()
    else:
        data_base = excecao.data_original.date()

    hora_inicio = excecao.hora_nova_inicio or evento.hora_inicio
    hora_fim = excecao.hora_nova_fim or evento.hora_fim

    return {
        'source_type': 'recorrente',
        'source_id': evento.id,
        'titulo': evento.titulo,
        'descricao': evento.descricao,
        'data_inicio': datetime.combine(data_base, hora_inicio).isoformat(),
        'data_fim': datetime.combine(data_base, hora_fim).isoformat() if hora_fim else None,
        'dia_semana': evento.dia_semana,
        'criado_por': evento.criado_por,
        'excecao_id': excecao.id,
        'remarcado': True,
    }