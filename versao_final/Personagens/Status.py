class Status():
    def __init__(self, status: dict) -> None:
        self.__vida_maxima = status['vida'] if 'vida' in status.keys() else 0
        self.__ataque = status['ataque'] if 'ataque' in status.keys() else 0
        self.__defesa = status['defesa'] if 'defesa' in status.keys() else 0
        self.__alcance = status['alcance'] if 'alcance' in status.keys() else 0
        self.__vel = status['vel'] if 'vel' in status.keys() else 0
        self.__vida = self.__vida_maxima
        self.__invencibilidade = False

    @property
    def ataque(self) -> int:
        return self.__ataque

    @ataque.setter
    def ataque(self, value: int) -> None:
        if type(value) == int and value > -1:
            self.__ataque = value

    @property
    def defesa(self) -> int:
        return self.__defesa

    @defesa.setter
    def defesa(self, value: int) -> None:
        if type(value) == int and value > -1:
            self.__defesa = value

    @property
    def alcance(self) -> int:
        return self.__alcance

    @alcance.setter
    def alcance(self, value: int) -> None:
        if type(value) == int and value > -1:
            self.__alcance = value

    @property
    def vida_maxima(self) -> int:
        return self.__vida_maxima

    @vida_maxima.setter
    def vida_maxima(self, value: int) -> None:
        if type(value) == int and value > -1:
            self.__vida_maxima = value

    @property
    def vida(self) -> int:
        return self.__vida

    @vida.setter
    def vida(self, value: int) -> None:
        if type(value) == int:
            self.__vida = value

    @property
    def vel(self) -> int:
        return self.__vel

    @vel.setter
    def vel(self, value: int) -> None:
        if type(value) == int:
            self.__vel = value

    @property
    def invencibilidade(self) -> bool:
        return self.__invencibilidade

    @invencibilidade.setter
    def invencibilidade(self, value):
        if type(value) == bool:
            self.__invencibilidade = value
