from abc import ABC, abstractmethod
from Utils.Hitbox import Hitbox
from Abstractions.AbstractPersonagem import AbstractPersonagem
from Enums.Enums import Direction, Estado
from pygame import Rect, Surface


class AbstractInimigo(AbstractPersonagem, ABC):
    def __init__(self, stats: dict, posicao: tuple, tamanho: tuple, terreno) -> None:
        self.__direction = Direction.MEIO_BAIXO
        self.__estado = Estado.REPOUSO

        self.__caminho = []
        self.__len_caminho = 0
        self.__estava_vendo_jogador = False
        self.__PERTO = 10
        self.__MINIMO_PASSOS_DADOS = 2
        self.__MINIMO_PASSOS_NO_CAMINHO = 0
        self.__view_distance = stats['view_distance'] if 'view_distance' in stats.keys() else 150

        super().__init__(stats, posicao, tamanho, terreno)

    @property
    def _estado(self) -> Estado:
        return self.__estado

    @property
    def direction(self) -> Direction:
        return self.__direction

    @abstractmethod
    def update(self, hit_jogador: Hitbox) -> None:
        if self.vida <= 0:
            self.__estado = Estado.MORRENDO
        super().update()

    def mover(self, hit_jogador: Hitbox) -> None:
        if self.__estado == Estado.MORRENDO:
            return None

        if self.__estado == Estado.REPOUSO:
            self.__update_visao(hit_jogador)
        elif self.__estado == Estado.ALERTA:
            self.__procurar_jogador(hit_jogador)
        elif self.__estado == Estado.ATACANDO:
            self.__seguir_jogador(hit_jogador)

    def get_rect_arma(self) -> Rect:
        posicao_frente = self.__determinar_posicao_frente()

        rect = Rect(posicao_frente, (self.alcance * 2, self.alcance * 2))
        rect.center = posicao_frente
        return rect

    @abstractmethod
    def atacar(self):
        if self.arma.atacar():
            return True
        else:
            return False

    @abstractmethod
    def morreu(self) -> bool:
        pass

    @property
    @abstractmethod
    def image(self) -> Surface:
        pass

    @property
    @abstractmethod
    def rect(self) -> Rect:
        pass

    def __seguir_jogador(self, hit_jogador: Hitbox) -> None:
        distancia = self._calcular_distancia(hit_jogador)
        if distancia < self.__PERTO:
            self.__dumb_movement(hit_jogador)

        # Se está vendo completamente, faz caminho burro
        if self.__esta_vendo_jogador_completamente(hit_jogador):
            self.__estava_vendo_jogador = True
            passos_dados = self.__len_caminho - len(self.__caminho)
            if passos_dados < self.__MINIMO_PASSOS_DADOS and len(self.__caminho) > 0:
                self.__mover_caminho()
            else:
                # Reseta flags de forçar andar em caminho possivelmente já calculados
                self.__caminho = []
                self.__MINIMO_PASSOS_NO_CAMINHO = 0
                self.__dumb_movement(hit_jogador)

        else:
            # Se está vendo parcialmente o jogador
            if self.__esta_vendo_jogador_minimamente(hit_jogador):
                self.__estava_vendo_jogador = True

                # Caso já tenha um caminho calculado e não perdeu visao do jogador força continuar o caminho antigo
                passos_dados = self.__len_caminho - len(self.__caminho)
                if len(self.__caminho) > 0 and passos_dados < self.__MINIMO_PASSOS_NO_CAMINHO:
                    self.__mover_caminho()
                else:
                    # Busca um novo caminho
                    novo_caminho = self.terreno.get_path(self.hitbox, hit_jogador.posicao)
                    self.__set_caminho(novo_caminho)
                    self.__mover_caminho()

            # Não possui visão do jogador
            else:
                # Se acabou de perder visão, busca o caminho para a ultima posição jogador
                if self.__estava_vendo_jogador:
                    self.__estava_vendo_jogador = False

                    novo_caminho = self.terreno.get_path(self.hitbox, hit_jogador.posicao)
                    self.__set_caminho(novo_caminho)
                    self.__mover_caminho()
                else:  # Segue a ultima posição conhecida do jogador
                    self.__mover_caminho()

    def __set_caminho(self, caminho) -> None:
        self.__len_caminho = len(caminho)
        self.__caminho = caminho

        if self.__len_caminho > 10:
            self.__MINIMO_PASSOS_NO_CAMINHO = 3
        elif self.__len_caminho > 7:
            self.__MINIMO_PASSOS_NO_CAMINHO = 2
        elif self.__len_caminho > 5:
            self.__MINIMO_PASSOS_NO_CAMINHO = 1

    def __procurar_jogador(self, hit_jogador: Hitbox) -> None:
        # Caso não tenha um caminho pega um aleatório
        if len(self.__caminho) == 0:
            self.__caminho = self.terreno.get_random_path(self.hitbox)

        # Procura o jogador
        if self.__encontrou_jogador_novamente(hit_jogador):
            self.__estado = Estado.ATACANDO
            self.__caminho = []
        else:
            # Se não, continua no caminho aleatório
            self.__mover_caminho()

    def __mover_caminho(self):
        if len(self.__caminho) > 0:
            proximo_ponto = self.__caminho[0]
            if self.__chegou_no_ponto(proximo_ponto):
                self.__caminho.pop(0)

            self.__mover_para_ponto(proximo_ponto)
        else:
            # Perdeu totalmente a visão do jogador e foi para o ultimo caminho
            # passa para estado de alerta, vai ficar procurando o jogador
            self.__estado = Estado.ALERTA

    def __chegou_no_ponto(self, ponto: tuple) -> bool:
        rect = Rect(self.hitbox.posicao, self.hitbox.tamanho)
        if rect.collidepoint(ponto):
            return True
        else:
            return False

    def __dumb_movement(self, hit_jogador: Hitbox) -> None:
        distancia = self._calcular_distancia(hit_jogador)

        rect_jogador = Rect(hit_jogador.posicao, hit_jogador.tamanho)
        if distancia < self.__PERTO:
            return self.__mover_para_o_centro(hit_jogador)
        else:
            destino = rect_jogador.topleft
            self.__mover_para_ponto(destino)

    def __mover_para_o_centro(self, hit_jogador: Hitbox) -> None:

        ponto = hit_jogador.center

        dist_x = abs(ponto[0] - self.hitbox.center[0])
        vel_x = self.vel if dist_x > self.vel else dist_x
        if ponto[0] > self.hitbox.center[0]:
            x_movement = vel_x
        elif ponto[0] < self.hitbox.center[0]:
            x_movement = -vel_x
        else:
            x_movement = 0

        dist_y = abs(ponto[1] - self.hitbox.center[1])
        vel_y = self.vel if dist_y > self.vel else dist_y
        if ponto[1] > self.hitbox.center[1]:
            y_movement = vel_y
        elif ponto[1] < self.hitbox.center[1]:
            y_movement = -vel_y
        else:
            y_movement = 0

        nova_posicao_x = (self.hitbox.x + x_movement, self.hitbox.y)
        if self.terreno.validar_movimento(personagem=self, posicao=nova_posicao_x):
            self.hitbox.posicao = nova_posicao_x

        nova_posicao_y = (self.hitbox.x, self.hitbox.y + y_movement)
        if self.terreno.validar_movimento(personagem=self, posicao=nova_posicao_y):
            self.hitbox.posicao = nova_posicao_y

        self.__atualizar_frente(x_movement, y_movement)

    def __mover_para_ponto(self, ponto: tuple) -> None:
        dist_x = abs(ponto[0] - self.hitbox.x)
        vel_x = self.vel if dist_x > self.vel else dist_x
        if ponto[0] > self.hitbox.x:
            x_movement = vel_x
        elif ponto[0] < self.hitbox.x:
            x_movement = -vel_x
        else:
            x_movement = 0

        dist_y = abs(ponto[1] - self.hitbox.y)
        vel_y = self.vel if dist_y > self.vel else dist_y
        if ponto[1] > self.hitbox.y:
            y_movement = vel_y
        elif ponto[1] < self.hitbox.y:
            y_movement = -vel_y
        else:
            y_movement = 0

        nova_posicao_x = (self.hitbox.x + x_movement, self.hitbox.y)
        if self.terreno.validar_movimento(personagem=self, posicao=nova_posicao_x):
            self.hitbox.posicao = nova_posicao_x

        nova_posicao_y = (self.hitbox.x, self.hitbox.y + y_movement)
        if self.terreno.validar_movimento(personagem=self, posicao=nova_posicao_y):
            self.hitbox.posicao = nova_posicao_y

        self.__atualizar_frente(x_movement, y_movement)

    def __update_visao(self, hit_jogador: Hitbox) -> None:
        if self.__estado == Estado.REPOUSO or self.__estado == Estado.ALERTA:
            if self.__jogador_dentro_da_visao(hit_jogador):
                if self.__esta_vendo_jogador_mediamente(hit_jogador):
                    self.__estado = Estado.ATACANDO

    def __encontrou_jogador_novamente(self, hit_jogador) -> bool:
        if self.__jogador_dentro_da_visao(hit_jogador):
            if self.__esta_vendo_jogador_minimamente(hit_jogador):
                return True

    def __jogador_dentro_da_visao(self, hit_jogador) -> bool:
        distancia = self._calcular_distancia(hit_jogador)
        if distancia < self.__view_distance:
            return True
        else:
            return False

    def __esta_vendo_jogador_minimamente(self, hit_jogador: Hitbox) -> bool:
        pares_pontos = [
            [self.hitbox.topleft, hit_jogador.topleft],
            [self.hitbox.bottomleft, hit_jogador.bottomleft],
            [self.hitbox.bottomright, hit_jogador.bottomright],
            [self.hitbox.topright, hit_jogador.topright]
        ]
        for par_ponto in pares_pontos:
            if self.terreno.is_line_of_sight_clear(par_ponto[0], par_ponto[1]):
                return True

        return False

    def __esta_vendo_jogador_completamente(self, hit_jogador: Hitbox) -> bool:
        pares_pontos = [
            [self.hitbox.topleft, hit_jogador.topleft],
            [self.hitbox.bottomleft, hit_jogador.bottomleft],
            [self.hitbox.bottomright, hit_jogador.bottomright],
            [self.hitbox.topright, hit_jogador.topright]
        ]
        quant = 0
        for par_ponto in pares_pontos:
            if self.terreno.is_line_of_sight_clear(par_ponto[0], par_ponto[1]):
                quant += 1

        if quant == 4:
            return True
        else:
            return False

    def __esta_vendo_jogador_mediamente(self, hit_jogador: Hitbox) -> bool:
        pontos = [hit_jogador.topleft, hit_jogador.topright,
                  hit_jogador.bottomleft, hit_jogador.bottomright]

        for ponto in pontos:
            if self.terreno.is_line_of_sight_clear(self.hitbox.center, ponto):
                return True
        return False

    def __atualizar_frente(self, x_movement, y_movement):
        if x_movement < 0:
            if y_movement < 0:
                #print('Esquerda Cima')
                self.__direction = Direction.ESQUERDA_CIMA
            elif y_movement > 0:
                #print('Esquerda Baixo')
                self.__direction = Direction.ESQUERDA_BAIXO
            else:
                #print('Esquerda Meio')
                self.__direction = Direction.ESQUERDA_MEIO
        elif x_movement > 0:
            if y_movement < 0:
                #print('Direita Cima')
                self.__direction = Direction.DIREITA_CIMA
            elif y_movement > 0:
                #print('Direita Baixo')
                self.__direction = Direction.DIREITA_BAIXO
            else:
                #print('Direita Meio')
                self.__direction = Direction.DIREITA_MEIO
        elif y_movement > 0:
            #print('Meio Baixo')
            self.__direction = Direction.MEIO_BAIXO
        elif y_movement < 0:
            #print('Meio Cima')
            self.__direction = Direction.MEIO_CIMA

    def _calcular_distancia(self, outro_hitbox: Hitbox):
        if self.__hitbox_encostado(outro_hitbox):
            return 0

        posicao1, posicao2 = self.__determinar_posicoes_mais_proximas(outro_hitbox)

        x = abs(posicao1[0] - posicao2[0]) ** 2
        y = abs(posicao1[1] - posicao2[1]) ** 2

        dist = (x + y)**(1/2)
        return dist

    def __hitbox_encostado(self, hitbox: Hitbox) -> bool:
        # Alinhados na horizontal
        if self.hitbox.left == hitbox.right or self.hitbox.right == hitbox.left:
            if self.hitbox.top > hitbox.top and self.hitbox.top < hitbox.bottom:
                return True
            elif hitbox.top > self.hitbox.top and hitbox.top < self.hitbox.bottom:
                return True
            else:
                return False
        # Alinhados na vertical
        elif self.hitbox.top == hitbox.bottom or self.hitbox.bottom == hitbox.top:
            if self.hitbox.right > hitbox.left and self.hitbox.right < hitbox.right:
                return True
            elif hitbox.right > self.hitbox.left and hitbox.right < self.hitbox.left:
                return True
            else:
                return False
        return False

    def __determinar_posicoes_mais_proximas(self, hit_jogador: Hitbox):
        if self.hitbox.x + self.hitbox.largura <= hit_jogador.x:  # A direita
            if self.hitbox.y + self.hitbox.altura < hit_jogador.y:  # Diagonal inferior
                return self.hitbox.bottomright, hit_jogador.topleft
            elif self.hitbox.y > hit_jogador.y + hit_jogador.altura:  # Diagonal Superior
                return self.hitbox.topright, hit_jogador.bottomleft
            else:  # Lado Direito
                return self.hitbox.midright, hit_jogador.midleft

        elif self.hitbox.x >= hit_jogador.x + hit_jogador.largura:  # A esquerda
            if self.hitbox.y > hit_jogador.y + hit_jogador.altura:  # Diagonal Superior
                return self.hitbox.topleft, hit_jogador.bottomright
            elif self.hitbox.y + self.hitbox.altura < hit_jogador.y:  # Diagonal Inferior
                return self.hitbox.bottomleft, hit_jogador.topright
            else:  # Lado Esquerdo
                return self.hitbox.midleft, hit_jogador.midright

        elif self.hitbox.y > hit_jogador.y:  # Acima
            return self.hitbox.midtop, hit_jogador.midbottom
        else:  # Abaixo
            return self.hitbox.midbottom, hit_jogador.midtop

    def __determinar_posicao_frente(self):
        if self.__direction == Direction.DIREITA_BAIXO:
            return self.hitbox.bottomright
        elif self.__direction == Direction.DIREITA_MEIO:
            return self.hitbox.midright
        elif self.__direction == Direction.DIREITA_CIMA:
            return self.hitbox.topright
        elif self.__direction == Direction.ESQUERDA_BAIXO:
            return self.hitbox.bottomleft
        elif self.__direction == Direction.ESQUERDA_MEIO:
            return self.hitbox.midleft
        elif self.__direction == Direction.ESQUERDA_CIMA:
            return self.hitbox.topleft
        elif self.__direction == Direction.MEIO_BAIXO:
            return self.hitbox.midbottom
        elif self.__direction == Direction.MEIO_CIMA:
            return self.hitbox.midtop
        else:
            return self.hitbox.midtop
