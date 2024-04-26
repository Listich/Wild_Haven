from os import walk

import pygame


def import_folder(path):
    Surface_list = []
    for _, _, img_files in walk(path):
        for image in img_files:
            full_path = path + '/' +image
            image_surf = pygame.image.load(full_path).convert_alpha()
            Surface_list.append(image_surf)
    return Surface_list