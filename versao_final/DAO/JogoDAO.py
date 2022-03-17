from DAO.DAO import DAO
from Controllers.Jogo import Jogo
from DAO.DAOAdapters import JogoDaoAdapter


class JogoDAO(DAO):
    def __init__(self) -> None:
        super().__init__('DAO/saves/saves')

    def add(self, jogo: Jogo) -> None:
        if isinstance(jogo, Jogo):
            jogo_dao = JogoDaoAdapter.add(jogo)
            save_name = jogo.save_name
            super().add(save_name, jogo_dao)

    def get(self, key: str) -> Jogo:
        if isinstance(key, str):
            jogo_dao = super().get(key)
            jogo = JogoDaoAdapter.create(jogo_dao)
            print(jogo.controlador.current_fase.current_map.jogador.hitbox.posicao)
            return jogo

    def remove(self, key: str) -> None:
        if isinstance(key, str):
            return super().remove(key)
