

class Botao:
    def __init__(self, posicao: tuple, tamanho: tuple, imagem: str, acao: str) -> None:
        self.__posicao = posicao
        self.__imagem = imagem
        self.__tamanho = tamanho
        self.__acao = acao
    
    @property
    def posicao(self):
        return self.__posicao
    
    @posicao.setter
    def posicao(self, posicao: tuple) -> None:
        if type(posicao) == tuple and len(posicao) == 2:
            self.__posicao = posicao
    
    @property
    def tamanho(self):
        return self.__tamanho
    
    @tamanho.setter
    def tamanho(self, tamanho: tuple) -> None:
        if type(tamanho) == tuple and len(tamanho) == 2:
            self.__tamanho = tamanho

    @property
    def imagem(self):
        return self.__imagem
    
    @imagem.setter
    def imagem(self, imagem):
        self.__imagem = imagem

    @property
    def acao(self):
        return self.__acao
    
    @acao.setter
    def acao(self, acao):
        if type(acao) == str:
            self.__acao = acao
