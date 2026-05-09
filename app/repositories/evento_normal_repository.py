from app.models.evento_normal import EventoNormal
from app.db.database import db

class EventoNormalRepository:
    def get_all(self):
        return EventoNormal.query.all()
    
    def get_by_id(self, id):
        return EventoNormal.query.filter_by(id=id).first()
    
    def create(self, dados):
        evento = EventoNormal(
            titulo=dados['titulo'],
            descricao=dados.get('descricao'),
            data_inicio=dados['data_inicio'],
            data_fim=dados.get('data_fim'),
            criado_por=dados['criado_por']
        )
        db.session.add(evento)
        db.session.commit()
        return evento
    
    def update(self, id, dados):
        evento = self.get_by_id(id)
        if not evento:
            return None
        # Atualiza apenas os campos enviados
        if 'titulo' in dados:
            evento.titulo = dados['titulo']
        if 'descricao' in dados:
            evento.descricao = dados.get('descricao')
        if 'data_inicio' in dados:
            evento.data_inicio = dados['data_inicio']
        if 'data_fim' in dados:
            evento.data_fim = dados.get('data_fim')
        if 'status' in dados:
            from . import EventoStatus  # noqa: F401
            # Convert string to enum if necessary
            if isinstance(dados['status'], str):
                from app.models.evento_normal import EventoStatus as ES
                try:
                    evento.status = ES[dados['status'].upper()]
                except KeyError:
                    raise ValueError('status inválido')
            else:
                evento.status = dados['status']
        # criado_por is immutable – ignore if present
        db.session.commit()
        return evento