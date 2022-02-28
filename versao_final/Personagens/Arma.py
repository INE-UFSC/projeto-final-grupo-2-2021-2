class Arma():
    def __init__(self, dano, alcance) -> None:
        self.__dano = dano
        self.__alcance = alcance
        self.__em_delay_ataque = False
        self.__desenhando_ataque = False

        self.__sprite_ataque = ''
        self.__timer_desenhando = 12
        self.__timer_delay = 30

    @property
    def desenhando_ataque(self) -> bool:
        return self.__desenhando_ataque

    @property
    def sprite_ataque(self) -> str:
        return self.__sprite_ataque

    @property
    def dano(self) -> int:
        return self.__dano

    @property
    def alcance(self) -> int:
        return self.__alcance

    @property
    def atacando(self) -> bool:
        return self.__em_delay_ataque

    def atacar(self) -> bool:
        if self.__em_delay_ataque:
            return False
        else:
            self.__em_delay_ataque = True
            self.__desenhando_ataque = True
            return True

    def update(self):
        if self.__em_delay_ataque:
            self.__timer_delay -= 1

            if self.__timer_delay < 0:
                self.__em_delay_ataque = False
                self.__timer_delay = 30

        if self.__desenhando_ataque:
            self.__timer_desenhando -= 1

            if self.__timer_desenhando < 0:
                self.__desenhando_ataque = False
                self.__timer_desenhando = 2
