from Pygame.src.setUp.settings import *
from os import walk
from os.path import join


def import_image(*path, alpha=True, format="png"):
    full_path = join(*path) + f'.{format}'
    return pygame.image.load(full_path).convert_alpha() if alpha else pygame.image.load(full_path).convert()


def import_folder(*path):
    frames = []
    for folder_path, sub_folders, image_names in walk(join(*path)):
        for image_name in sorted(image_names, key=lambda x: int(x.split('.')[0])):
            full_path =  join(folder_path, image_name)
            frames.append(pygame.image.load(full_path).convert_alpha())
    return frames


def import_folder_dict(*path):
    frames = {}
    for folder_path, _, image_names in walk(join(*path)):
        for image_name in image_names:
            full_path = join(folder_path, image_name)
            surface = pygame.image.load(full_path).convert_alpha()
            frames[image_name.split('.')[0]] = surface
    return frames


def import_sub_folders(*path):
    frames = {}
    for _, sub_folders, _ in walk(join(*path)):
        if sub_folders:
            for sub_folder in sub_folders:
                frames[sub_folder] = import_folder_dict(*path, sub_folder)
    return frames

