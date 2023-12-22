import math

import pygame

from DataBase import Base


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


def filling_table(x, y, height, width, sid):
    table = [[] for _ in range(NUM_OF_CELLS_CHUNK)]
    for h in range(y, height + y):
        for w in range(x, width + x):
            if y != 0:
                res = h % abs(y)
            else:
                res = h
            table[res].append(get_bioms(perlig_noise(h, w, sid)))
    return table


def perlig_noise(x, y, sid):
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


def join_table(list_table, direction='width'):
    if direction == 'width':
        result = [[] for _ in range(len(list_table[0]))]
        for i in range(len(list_table)):
            for j in range(len(list_table[i])):
                result[j] += (list_table[i][j])
    elif direction == 'height':
        result = []
        for i in range(len(list_table)):
            result += list_table[i]
    return result


class Biom:
    def __init__(self, name, color, min_altitude, max_altitude):
        self.name = name
        self.color = color
        self.min_altitude = min_altitude
        self.max_altitude = max_altitude

    def get_color(self):
        return self.color

    def get_min_altitude(self):
        return self.min_altitude

    def get_max_altitude(self):
        return self.max_altitude


class Map:
    def __init__(self, height, width, cell_size, sid, load_chunk=1):
        self.width = width
        self.height = height
        self.chunks = []
        self.board = []
        for i in range(0, 3):
            for j in range(0, 3):
                self.chunks.append(Chunk(i, -NUM_OF_CELLS_CHUNK + NUM_OF_CELLS_CHUNK * j,
                                         -NUM_OF_CELLS_CHUNK + NUM_OF_CELLS_CHUNK * i, sid))
        for i in range(3):
            self.board.append(join_table(list(i.get_chunk() for i in self.chunks[3 * i:3 * (i + 1)])))
        self.board = join_table(self.board, direction='height')

        self.cell_size = cell_size

    def render(self, screen):
        for height in range(self.height):
            for width in range(self.width):
                left, top = width * self.cell_size, height * self.cell_size
                color = BIOMS[self.board[height][width]].get_color()
                pygame.draw.rect(screen, pygame.Color(color), [left, top, self.cell_size, self.cell_size])


class Chunk:
    def __init__(self, id, x, y, sid):
        self.id = id
        self.x, self.y = x, y
        self.table = filling_table(x, y, NUM_OF_CELLS_CHUNK, NUM_OF_CELLS_CHUNK, sid)

    def get_chunk(self):
        return self.table

    def get_coord(self):
        return self.x, self.y

    def get_id(self):
        return self.id


def get_bioms(altitude):
    return bd.get_all_information('id', 'Bioms', f'min_altitude <= {altitude} and {altitude} <= max_altitude')[0][0]


bd = Base()
NUM_OF_CELLS_CHUNK = 64
BIOMS = {}
CHUNKS = {}
for biom in bd.get_all_information('*', 'Bioms'):
    id, name, color, min_altitude, max_altitude = (j for j in biom)
    BIOMS[id] = Biom(name, color, min_altitude, max_altitude)

#           ! ! !       ! ! !       ! ! !
#           ! 1 2       1 2 3       2 3 !
#           ! 4 5       4 5 6       5 6 !

#           ! 1 2       1 2 3       2 3 !
#           ! 4 5       4 5 6       5 6 !
#           ! 7 8       7 8 9       8 9 !

#           ! 4 5       4 5 6       5 6 !
#           ! 7 8       7 8 9       8 9 !
#           ! ! !       ! ! !       ! ! !
