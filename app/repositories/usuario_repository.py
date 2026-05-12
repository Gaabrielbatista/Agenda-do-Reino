import bcrypt
from sqlalchemy.exc import IntegrityError

from app.models.usuario import Usuario, UserType
from app.db.database import db


def _hash_senha(senha: str) -> str:
    return bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


def _validate_tipo(value: str) -> UserType:
    try:
        return UserType[value.upper()]
    except (KeyError, AttributeError):
        valores = [e.name.lower() for e in UserType]
        raise ValueError(f"tipo inválido: '{value}'. Valores aceitos: {valores}")


class UsuarioRepository:
    def get_all(self):
        return Usuario.query.all()

    def get_by_id(self, id):
        return Usuario.query.filter_by(id=id).first()

    def get_by_email(self, email):
        return Usuario.query.filter_by(email=email).first()

    def create(self, dados):
        usuario = Usuario(
            nome=dados['nome'],
            email=dados['email'].lower().strip(),
            senha_hash=_hash_senha(dados['senha']),
            tipo=_validate_tipo(dados['tipo']),
        )
        try:
            db.session.add(usuario)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            raise ValueError(f"Email '{dados['email']}' já está em uso")
        return usuario

    def update(self, usuario: Usuario, dados: dict) -> Usuario:
        """Recebe o objeto já carregado — sem query extra."""
        if 'nome' in dados:
            usuario.nome = dados['nome']
        if 'email' in dados:
            novo_email = dados['email'].lower().strip()
            if novo_email != usuario.email:
                existente = self.get_by_email(novo_email)
                if existente:
                    raise ValueError(f"Email '{dados['email']}' já está em uso")
                usuario.email = novo_email
        if 'senha' in dados:
            usuario.senha_hash = _hash_senha(dados['senha'])
        if 'tipo' in dados:
            usuario.tipo = _validate_tipo(dados['tipo'])
        db.session.commit()
        return usuario

    def delete(self, usuario: Usuario) -> None:
        """Recebe o objeto já carregado — sem query extra."""
        db.session.delete(usuario)
        db.session.commit()