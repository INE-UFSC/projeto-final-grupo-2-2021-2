from abstractions.AbstractItem import AbstractItem


class PocaoPequena(AbstractItem):
    def vida(self, vida_atual):
        return vida_atual + 3

    def velocidade(self, velocidade):
        return velocidade

    def defesa(self, defesa):
        return defesa

    def vida_maxima(self, vida_maxima):
        return vida_maxima

    def dano(self, dano):
        return dano

    def invencibilidade(self) -> bool:
        return False
