from os import walk
import pygame


def import_folder(path: str, size: tuple) -> list:
    surface_list = []
    for _, _, image_files in walk(path):
        for image_name in image_files:
            full_path = f'{path}/{image_name}'
            image_surf = pygame.image.load(full_path).convert_alpha()
            # image_surf = pygame.transform.flip(image_surf, True, False)
            image_surf = pygame.transform.scale(image_surf, size)

            surface_list.append(image_surf)

    return surface_list


def import_fliped_folder(path: str, size: tuple) -> list:
    surface_list = []
    for _, _, image_files in walk(path):
        for image_name in image_files:
            full_path = f'{path}/{image_name}'
            image_surf = pygame.image.load(full_path).convert_alpha()
            image_surf = pygame.transform.flip(image_surf, True, False)
            image_surf = pygame.transform.scale(image_surf, size)

            surface_list.append(image_surf)

    return surface_list
