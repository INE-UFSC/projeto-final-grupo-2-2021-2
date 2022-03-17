from typing import List, Type
from Controllers.ControladorFases import ControladorFases
from Controllers.Jogo import Jogo
from Fases.AbstractFase import AbstractFase
from Personagens.AbstractInimigo import AbstractInimigo
from Mapas.AbstractMapa import AbstractMapa
from Personagens.Jogador import Jogador
from Personagens.Status import Status
from Utils.Hitbox import Hitbox


class InimigosDaoAdapter:
    @classmethod
    def add(cls, enemy: AbstractInimigo) -> dict:
        enemy_dao = {}
        if isinstance(enemy, AbstractInimigo):
            enemy_dao['hitbox'] = enemy.hitbox
            enemy_dao['status'] = enemy.status
            enemy_dao['type'] = type(enemy)
            return enemy_dao

    @classmethod
    def create(cls, enemy_dao: dict, mapa: AbstractMapa) -> AbstractInimigo:
        Tipo: Type[AbstractInimigo] = enemy_dao['type']
        status: Status = enemy_dao['status']
        hitbox: Hitbox = enemy_dao['hitbox']

        enemy: AbstractInimigo = Tipo(posicao=hitbox.posicao, mapa=mapa)
        enemy.set_hitbox(hitbox)
        enemy.status = status
        return enemy


class JogadorDaoAdapter:
    @classmethod
    def add(cls, jogador: Jogador) -> dict:
        jogador_dao = {}
        if isinstance(jogador, Jogador):
            jogador_dao['hitbox'] = jogador.hitbox
            jogador_dao['status'] = jogador.status
            return jogador_dao

    @classmethod
    def create(cls, jogador_dao: dict) -> Jogador:
        status: Status = jogador_dao['status']
        hitbox: Hitbox = jogador_dao['hitbox']

        jogador = Jogador((0, 0))
        jogador.set_hitbox(hitbox)
        jogador.status = status

        return jogador


class MapDaoAdapter:
    @classmethod
    def add(cls, mapa: AbstractMapa) -> dict:
        mapa_dao = {}
        if isinstance(mapa, AbstractMapa):
            inimigos = mapa.inimigos
            inimigos_dao = []
            for inimigo in inimigos:
                inimigo_dao = InimigosDaoAdapter.add(inimigo)
                inimigos_dao.append(inimigo_dao)
            jogador_dao = JogadorDaoAdapter.add(mapa.jogador)

            mapa_dao['enemies'] = inimigos_dao
            mapa_dao['jogador'] = jogador_dao
            mapa_dao['type'] = type(mapa)
            return mapa_dao

    @classmethod
    def create(cls, mapa_dao: dict) -> AbstractMapa:
        jogador_dao = mapa_dao['jogador']
        enemies_dao = mapa_dao['enemies']
        MapTipo: Type[AbstractMapa] = mapa_dao['type']

        jogador = JogadorDaoAdapter.create(jogador_dao)
        mapa = MapTipo(jogador)
        mapa.load()
        enemies = []
        for enemy_dao in enemies_dao:
            enemy = InimigosDaoAdapter.create(enemy_dao, mapa)
            enemies.append(enemy)

        list_hitbox = []
        for enemy in enemies:
            list_hitbox.append(enemy.hitbox)

        mapa.add_inimigos(enemies)
        for inimigo in mapa.inimigos:
            hitbox = list_hitbox.pop(0)
            inimigo.set_hitbox(hitbox)

        return mapa


class FaseDaoAdapter:
    @classmethod
    def add(cls, fase: AbstractFase) -> dict:
        fase_dao = {}
        if isinstance(fase, AbstractFase):
            mapas = fase.mapas
            mapas_dao = []
            for mapa in mapas:
                mapa_dao = MapDaoAdapter.add(mapa)
                mapas_dao.append(mapa_dao)

            jogador_dao = JogadorDaoAdapter.add(fase.jogador)
            fase_dao['mapas'] = mapas_dao
            fase_dao['type'] = type(fase)
            fase_dao['jogador'] = jogador_dao
            fase_dao['map_index'] = fase.current_map_index
            return fase_dao

    @classmethod
    def create(cls, fase_dao: dict) -> AbstractFase:
        FaseType: Type[AbstractFase] = fase_dao['type']
        jogador_dao: dict = fase_dao['jogador']
        mapa_index: int = fase_dao['map_index']
        mapas_dao = dict = fase_dao['mapas']

        jogador = JogadorDaoAdapter.create(jogador_dao)
        mapas: List[AbstractMapa] = []

        for mapa_dao in mapas_dao:
            # print('Criando um mapa')
            mapa = MapDaoAdapter.create(mapa_dao)
            mapas.append(mapa)

        # print('Criando Fase')
        fase = FaseType(jogador)
        # print('Pronto')
        for mapa in mapas:
            mapa.jogador = jogador
            mapa.load()

        current_map = mapas[mapa_index]
        jogador.mapa = current_map

        fase.mapas = mapas
        fase.current_map_index = mapa_index

        return fase


class ControladorFasesDaoAdapter:
    @classmethod
    def add(cls, controlador: ControladorFases) -> dict:
        controlador_dao = {}
        if isinstance(controlador, ControladorFases):
            fases = controlador.fases
            current_fase = controlador.current_fase
            current_fase_dao = FaseDaoAdapter.add(current_fase)

            fases_dao = []
            for fase in fases:
                fase_dao = FaseDaoAdapter.add(fase)
                fases_dao.append(fase_dao)

            controlador_dao['fases'] = fases_dao
            controlador_dao['current'] = current_fase_dao
            return controlador_dao

    @classmethod
    def create(cls, controlador_dao: dict) -> ControladorFases:
        fases_dao = controlador_dao['fases']
        fases = []
        for fase_dao in fases_dao:
            # print('Criando aqui')
            fase = FaseDaoAdapter.create(fase_dao)
            jogador = fase.jogador
            fases.append(fase)

        current_fase_dao = controlador_dao['current']
        current_fase = FaseDaoAdapter.create(current_fase_dao)
        jogador = current_fase.jogador

        # print('Criando Controlador')
        controlador = ControladorFases(jogador)
        controlador.current_fase = current_fase
        controlador.set_fases(fases)

        return controlador


class JogoDaoAdapter:
    @classmethod
    def add(cls, jogo: Jogo) -> dict:
        jogo_dao = {}
        if isinstance(jogo, Jogo):
            controlador = jogo.controlador
            controlador_dao = ControladorFasesDaoAdapter.add(controlador)
            jogo_dao['controlador'] = controlador_dao
            jogo_dao['name'] = jogo.save_name

            return jogo_dao

    @classmethod
    def create(cls, jogo_dao: dict) -> Jogo:
        controlador_dao = jogo_dao['controlador']
        save_name = jogo_dao['name']
        controlador = ControladorFasesDaoAdapter.create(controlador_dao)

        jogo = Jogo(save_name)
        jogo.controlador = controlador

        # print('Retornando Jogo')
        return jogo
