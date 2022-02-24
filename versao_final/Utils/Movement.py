from math import atan2, degrees, pi


def gerar_equação_vetorial_reta(p1, p2):
    def funcao(x):
        sub = ((p2[0] - p1[0]) * x, (p2[1] - p1[1]) * x)
        ponto = (p1[0] + sub[0], p1[1] + sub[1])
        return ponto

    return funcao
