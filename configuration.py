import os
import sys

def load_config(*args):
    global data
    filename = os.path.join('config', "cfg.txt")
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
        config.write("anySaves=0\n")
        config.write("difficult=1\n")
        config = open(filename, "r+")
        data = {item.split("=")[0]: int(item.split("=")[1]) for item in config.read()[:-1].split("\n")}
    config.close()
    return data