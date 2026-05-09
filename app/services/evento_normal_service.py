from app.repositories.evento_normal_repository import EventoNormalRepository

class EventoNormalService:
    def __init__(self):
        self.repository = EventoNormalRepository()
    
    def listar_todos(self):
        return self.repository.get_all( )