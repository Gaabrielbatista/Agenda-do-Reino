from app.repositories.evento_normal_repository import EventoNormalRepository

class EventoNormalService:
    def __init__(self):
        self.repository = EventoNormalRepository()
    
    def get_all(self):
        return self.repository.get_all( )

    def get_by_id(self, id):
        return self.repository.get_by_id(id)
    
    def create(self, dados):
        return self.repository.create(dados)
    
    def update(self, id, dados):
        evento = self.repository.get_by_id(id)

        if not evento:
            return None

        updated = self.repository.update(id, dados)

        return updated
