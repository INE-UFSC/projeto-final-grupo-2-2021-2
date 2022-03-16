from typing import Any
from DAO.DAO import DAO
from Controllers.Jogo import Jogo


class JogoDAO(DAO):
    def __init__(self) -> None:
        super().__init__('DAO/saves/saves')

    def add(self, jogo: Jogo) -> None:
        if isinstance(jogo, Jogo):
            key = jogo.save_name
            super().add(key, jogo)

    def get(self, key: str) -> Any:
        if isinstance(key, str):
            return super().get(key)

    def remove(self, key: str) -> None:
        if isinstance(key, str):
            return super().remove(key)
