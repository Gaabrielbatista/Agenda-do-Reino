from datetime import datetime

from app.repositories.evento_excecao_repository import EventoExcecaoRepository
from app.repositories.evento_recorrente_repository import EventoRecorrenteRepository


class EventoExcecaoService:
    def __init__(self):
        self.repository = EventoExcecaoRepository()
        self.recorrente_repo = EventoRecorrenteRepository()

    def get_all(self):
        return self.repository.get_all()

    def get_by_id(self, id):
        return self.repository.get_by_id(id)

    def get_by_recorrente(self, evento_recorrente_id: int):
        return self.repository.get_by_recorrente(evento_recorrente_id)

    def create(self, dados: dict):
        # Valida que o evento recorrente existe
        recorrente_id = dados['evento_recorrente_id']
        recorrente = self.recorrente_repo.get_by_id(recorrente_id)
        if not recorrente:
            raise ValueError(f"EventoRecorrente id={recorrente_id} não encontrado")

        # Valida que não existe exceção duplicada para a mesma ocorrência
        data_original = datetime.fromisoformat(dados['data_original'])
        existente = self.repository.get_by_recorrente_e_data(recorrente_id, data_original)
        if existente:
            raise ValueError(
                f"Já existe uma exceção para o evento {recorrente_id} "
                f"na data {data_original.isoformat()}"
            )

        return self.repository.create(dados)

    def update(self, id: int, dados: dict):
        excecao = self.repository.get_by_id(id)
        if not excecao:
            return None
        return self.repository.update(excecao, dados)

    def delete(self, id: int) -> bool:
        excecao = self.repository.get_by_id(id)
        if not excecao:
            return False
        self.repository.delete(excecao)
        return True