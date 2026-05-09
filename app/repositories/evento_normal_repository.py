from app.models.evento_normal import EventoNormal

class EventoNormalRepository:
    def get_all(self):
        return EventoNormal.query.all()