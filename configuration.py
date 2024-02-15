import os
import sys
import pygame

def load_image(name, folder, colorkey=None):
    fullname = os.path.join(f"data\{folder}", name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(f"data/{folder}" + "/" + name)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def load_config(*args):
    global data
    filename = os.path.join('data/config', "cfg.txt")
    config = open(filename, "r+")
    raw_data = config.read()[:-1]
    if raw_data and args:
        data = {item.split("=")[0]: int(item.split("=")[1]) for item in raw_data.split("\n")}
        if args[1] == "res":
            config = open(filename, "w")
            config.write(f"resolutionWidth={args[0][0]}\n")
            config.write(f"resolutionHeight={args[0][1]}\n")
            config.write(f"anySaves={data['anySaves']}\n")
            config.write(f"difficult={data['difficult']}\n")
            config = open(filename, "r+")
            data = {item.split("=")[0]: int(item.split("=")[1]) for item in config.read()[:-1].split("\n")}
        if args[1] == "dif":
            config = open(filename, "w")
            config.write(f"resolutionWidth={data['resolutionWidth']}\n")
            config.write(f"resolutionHeight={data['resolutionHeight']}\n")
            config.write(f"anySaves={data['anySaves']}\n")
            config.write(f"difficult={args[0]}\n")
            config = open(filename, "r+")
            data = {item.split("=")[0]: int(item.split("=")[1]) for item in config.read()[:-1].split("\n")}
    else:
        config = open(filename, "w")
        config.write("resolutionWidth=1280\n")
        config.write("resolutionHeight=720\n")
        if os.listdir(path='data/saves'):
            config.write("anySaves=1\n")
        else:
            config.write("anySaves=0\n")
        config.write("difficult=1\n")
        config = open(filename, "r+")
        data = {item.split("=")[0]: int(item.split("=")[1]) for item in config.read()[:-1].split("\n")}
    config.close()
    return data


NUM_OF_CELLS_CHUNK = 31
cell_size = 20