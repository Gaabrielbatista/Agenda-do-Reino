from app.repositories.usuario_repository import UsuarioRepository


class UsuarioService:
    def __init__(self):
        self.repository = UsuarioRepository()

    def get_all(self):
        return self.repository.get_all()

    def get_by_id(self, id):
        return self.repository.get_by_id(id)

    def create(self, dados):
        return self.repository.create(dados)

    def update(self, id, dados):
        usuario = self.repository.get_by_id(id)
        if not usuario:
            return None
        return self.repository.update(usuario, dados)

    def delete(self, id) -> bool:
        usuario = self.repository.get_by_id(id)
        if not usuario:
            return False
        self.repository.delete(usuario)
        return True