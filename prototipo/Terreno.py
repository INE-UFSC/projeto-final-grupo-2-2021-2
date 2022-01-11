from abc import ABC, abstractmethod

class Terreno(ABC):
    def __init__(self,personagens,item,hitbox):
        self.__personagens = personagens
        self.__item = item
        self.__hitbox  = hitbox

    @abstractmethod
    def dropar_item():
        pass

    @abstractmethod
    def remover_inimigo():
        pass

    @abstractmethod
    def validar_movimento():
        pass

    @abstractmethod
    def iniciar_rodada():
        pass

    