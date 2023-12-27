import math

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
    table = [[] for _ in range(height)]
    for h in range(y, height + y):
        for w in range(x, width + x):
            if y != 0:
                res = h % abs(y)
            else:
                res = h
            table[res].append(get_bioms(perlig_noise(h, w, sid)))
    return table


def perlig_noise(x, y, sid):
    x, y = abs(x), abs(y)
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
    result = []
    if direction == 'width':
        result = [[] for _ in range(len(list_table[0]))]
        for i in range(len(list_table)):
            for j in range(len(list_table[i])):
                result[j] += (list_table[i][j])
    elif direction == 'height':
        for i in range(len(list_table)):
            result += list_table[i]
    return result


def get_bioms(altitude):
    res = bd.get_all_information('id', 'Bioms', f'min_altitude <= {altitude} and {altitude} <= max_altitude')
    if res:
        return res[0][0]
    return 0


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


bd = Base()
BIOMS = {}
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
