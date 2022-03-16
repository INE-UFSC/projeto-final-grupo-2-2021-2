import pygame
from Utils.Folder import import_folder, import_single_sprite
from pygame.sprite import Sprite
from DAO.DAO import DAO


class Teste(Sprite):

    def __init__(self) -> None:
        pygame.init()
        super().__init__()
        self.image = pygame.image.load('Assets/Telas/1.jpg')


janela = pygame.display.set_mode((500, 500))
imagem_fundo = pygame.image.load('Assets/Telas/1.jpg')


teste1 = Teste()

dao = DAO()
dao.add('Key', teste1)
