import math
import pygame


def findnoise2(x, y):
    n = int(x) + int(y) * 57
    allf = 0xFFFFFFFF
    an = (n << 13) & allf
    n = (an ^ n) & allf
    nn = (n * (n * n * 60493 + 19990303) + 1376312589) & 0x7fffffff
    return 1.0 - (float(nn) / 1073741824.0)


def interpolate(a, b, x):
    ft = float(x * 3.1415927)
    f = float((1.0 - math.cos(ft)) * 0.5)
    return a * (1.0 - f) + b * f


def noise(x, y):
    floorx = int(x)
    floory = int(y)
    s = findnoise2(floorx, floory)
    t = findnoise2(floorx + 1, floory)
    u = findnoise2(floorx, floory + 1)
    v = findnoise2(floorx + 1, floory + 1)
    int1 = interpolate(s, t, x - floorx)
    int2 = interpolate(u, v, x - floorx)
    return interpolate(int1, int2, y - floory)


def filling_table(height, width, sid):
    table = [[0 for _ in range(width)] for _ in range(height)]
    for h in range(0, height):
        for w in range(0, width):
            table[h][w] = f(h, w, sid)
    return table


def f(x, y, sid):
    #  sid = [2, 4, 8]
    scale1 = sid[0] / 10
    scale2 = sid[1] / 10
    scale3 = sid[2] / 10
    meaning = int((noise(x / scale1, y / scale1) + 1.0) * 42)
    meaning += int((noise(x / scale2, y / scale2) + 1.0) * 42)
    meaning += int((noise(x / scale3, y / scale3) + 1.0) * 42)
    if meaning > 255:
        meaning = 255
    elif meaning < 0:
        meaning = 0
    return meaning


class biom:
    def __init__(self, name, altitude, color):
        self.name = name
        self.color = color
        self.altitude = altitude

    def get_color(self, h):
        if self.altitude[0] <= h <= self.altitude[1]:
            return self.color
        return False


class Map:
    def __init__(self, height, width, cell_size, sid):
        self.width = width
        self.height = height
        self.board = filling_table(height, width, sid)
        self.left = 0
        self.top = 0
        self.cell_size = cell_size

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen):
        for height in range(self.height):
            for width in range(self.width):
                left, top = self.left + width * self.cell_size, self.top + height * self.cell_size
                for i in BIOM:
                    color = BIOM[i].get_color(self.board[height][width])
                    if color:
                        pygame.draw.rect(screen, color, [left, top, self.cell_size, self.cell_size])

    def get_cell(self, mouse_pos):
        if self.left <= mouse_pos[0] <= self.left + self.cell_size * self.height and \
                self.top <= mouse_pos[1] <= self.top + self.cell_size * self.width:
            num_w, num_h = (mouse_pos[0] - self.left) // self.cell_size, (mouse_pos[1] - self.top) // self.cell_size,
            return num_h, num_w
        return None

    def on_click(self, cell_coords):
        if cell_coords is not None:
            x, y = cell_coords[0], cell_coords[1]

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        self.on_click(cell)


BIOM = {'Sea': biom('sea', (0, 99), 'blue'),
    'Beach': biom('beach', (100, 119), 'yellow'),
    'Meadows': biom('meadows', (120, 139), 'green'),
    'forest': biom('forest', (140, 179), 'darkgreen'),
    'stone': biom('stone', (180, 210), 'grey'),
    'mountains': biom('mountains', (210, 255), 'white')}
