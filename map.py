import pygame
from random import sample, choice

from map_generation import filling_table, join_table, BIOMS
from configuration import NUM_OF_CELLS_CHUNK, cell_size
from configuration import load_config, load_image
from object import random_enemy


def play_ambient():
    data = load_config()
    ambient = choice(["ambient1.mp3", "ambient2.mp3", "ambient3.mp3", "ambient4.mp3"])
    pygame.mixer.music.load(f"data/music/{ambient}")
    pygame.mixer.music.set_volume(data["volume"]/100)
    pygame.mixer.music.play(-1)


class Map:
    def __init__(self, sid, start_coord=(0, 0)):
        self.size = NUM_OF_CELLS_CHUNK * 3
        self.start_x, self.start_y = start_coord[0], start_coord[1]
        self.sid = sid
        self.chunk_id = 0
        self.chunks = []
        self.board = []
        self.impenetrable = []
        for i in [-1.5, -0.5, 0.5]:
            self.chunks.append([])
            for j in [-1.5, -0.5, 0.5]:
                x, y = int(self.start_x + NUM_OF_CELLS_CHUNK * j), int(self.start_y + NUM_OF_CELLS_CHUNK * i)
                CHUNKS[(x, y)] = Chunk(self.chunk_id, x, y, self.sid)
                self.chunks[-1].append(CHUNKS[(x, y)])
                self.chunk_id += 1
        self.loading_map()
        self.enemy = []

    def render(self, screen, pos):
        x = pos[0]
        y = pos[1]
        for height in range(NUM_OF_CELLS_CHUNK + y, NUM_OF_CELLS_CHUNK * 2 + y):
            for width in range(NUM_OF_CELLS_CHUNK + x, NUM_OF_CELLS_CHUNK * 2 + x):
                left = (width - NUM_OF_CELLS_CHUNK - x) * cell_size
                top = (height - NUM_OF_CELLS_CHUNK - y) * cell_size
                biom = BIOMS[self.board[height][width]]
                base_sprite = biom.get_base()
                advanced_sprite = biom.get_advanced()
                rect = pygame.Rect(self.get_start_chunks()[0] + width + 1, self.get_start_chunks()[1] + height + 1, cell_size, cell_size)
                if not biom.get_passability() and rect not in self.impenetrable:
                    self.impenetrable.append(rect)
                pygame.draw.rect(screen, pygame.Color(0, 0, 0), [left, top, cell_size, cell_size])
                screen.blit(pygame.transform.scale(load_image(base_sprite, "sprites"),
                                                   (cell_size, cell_size)), (left, top))
                screen.blit(pygame.transform.scale(load_image(advanced_sprite, "sprites"),
                                                   (cell_size, cell_size)), (left, top))

    def loading_map(self):
        self.board = []
        for list_chunks in self.chunks:
            self.board.append(join_table(list(chunk.get_chunk() for chunk in list_chunks)))
        self.board = join_table(self.board, direction='height')
        self.graph = creat_graph(self.board)

    def chunk_update(self, pos):
        x, y = pos[0], pos[1]
        if abs(x) > NUM_OF_CELLS_CHUNK // 2:
            coof = 0 if x < NUM_OF_CELLS_CHUNK // 2 else -1
            for i in range(len(self.chunks)):
                x = self.chunks[i][coof].get_coords()[0] - (NUM_OF_CELLS_CHUNK if not coof else - NUM_OF_CELLS_CHUNK)
                y = self.chunks[i][coof].get_coords()[1]
                if not CHUNKS.get((x, y)):
                    CHUNKS[(x, y)] = Chunk(self.chunk_id, x, y, self.sid, enemy=True)
                    self.chunk_id += 1

                new_chunk = CHUNKS[(x, y)]
                self.chunks[i] = [new_chunk] + self.chunks[i][:2] if not coof else self.chunks[i][1:] + [new_chunk]
        else:
            new_chunks = [[]]
            coof = 0 if y < NUM_OF_CELLS_CHUNK // 2 else -1

            for chunk in self.chunks[coof]:
                x = chunk.get_coords()[0]
                y = chunk.get_coords()[1] - NUM_OF_CELLS_CHUNK if not coof \
                    else chunk.get_coords()[1] + NUM_OF_CELLS_CHUNK
                if not CHUNKS.get((x, y)):
                    CHUNKS[(x, y)] = Chunk(self.chunk_id, x, y, self.sid, enemy=True)
                    self.chunk_id += 1
                new_chunks[0].append(CHUNKS[(x, y)])
            self.chunks = new_chunks + self.chunks[:2] if not coof else self.chunks[1:] + new_chunks

        self.loading_map()
        self.enemy_update()

    def enemy_update(self):
        self.enemy = []
        for chunks in self.chunks:
            for chunk in chunks:
                self.enemy.append(chunk.get_enemy())

    def get_coord(self, x, y):
        x, y = int(x - self.get_start_chunks()[0] - 1), int(y - self.get_start_chunks()[1] - 1)
        return x, y

    def get_chunks(self):
        return self.chunks

    def get_board(self):
        return self.board

    def get_enemy(self):
        return self.enemy

    def get_start_chunks(self):
        return self.chunks[0][0].get_coords()

    def get_graph(self):
        return self.graph

    def get_impenetrable(self):
        return self.impenetrable


class Chunk:
    def __init__(self, id_chunk, x, y, sid, enemy=False):
        self.id = id_chunk
        self.x, self.y = x, y
        self.num = NUM_OF_CELLS_CHUNK
        self.table = filling_table(x, y, NUM_OF_CELLS_CHUNK, NUM_OF_CELLS_CHUNK, sid)
        self.enemy = []
        if enemy:
            self.spawn_enemy(4)   # Кол-во будет зависеть от сложности

    def spawn_enemy(self, count_enemy):
        x = sample(range(self.x, self.x + self.num), count_enemy)
        y = sample(range(self.y, self.y + self.num), count_enemy)
        self.enemy = [(x[i], y[i]) for i in range(count_enemy)]
        self.enemy = random_enemy(self.enemy)

    def get_chunk(self):
        return self.table

    def get_coords(self):
        return self.x, self.y

    def get_id(self):
        return self.id

    def get_enemy(self):
        return self.enemy


class Camera:
    def __init__(self, map_object, pos):
        self.pos = pos
        self.map_object = map_object
        play_ambient()

    def move(self, direction, moving):
        directions = {'North': (0, -1), 'South': (0, 1), 'East': (1, 0), 'West': (-1, 0)}
        if moving:
            self.pos = [self.pos[0] + directions[direction][0], self.pos[1] + directions[direction][1]]

    def get_pos(self):
        if self.pos[0] > NUM_OF_CELLS_CHUNK // 2:
            self.map_object.chunk_update(self.pos)
            self.pos[0] = -self.pos[0] + 1

        elif self.pos[0] < -(NUM_OF_CELLS_CHUNK // 2):
            self.map_object.chunk_update(self.pos)
            self.pos[0] = -self.pos[0] - 1

        elif self.pos[1] > NUM_OF_CELLS_CHUNK // 2:
            self.map_object.chunk_update(self.pos)
            self.pos[1] = -self.pos[1] + 1

        elif self.pos[1] < -(NUM_OF_CELLS_CHUNK // 2):
            self.map_object.chunk_update(self.pos)
            self.pos[1] = -self.pos[1] - 1

        return self.pos


def creat_graph(grid):

    def check_next_node(x, y):
        if 0 <= x < NUM_OF_CELLS_CHUNK * 3 and 0 <= y < NUM_OF_CELLS_CHUNK * 3:
            return BIOMS[grid[y][x]].get_passability()
        return False

    def get_next_nodes(x, y):
        if not check_next_node(x, y):
            return []
        ways = [-1, 0], [0, -1], [1, 0], [0, 1]
        return [(x + dx, y + dy) for dx, dy in ways if check_next_node(x + dx, y + dy)]

    graph = {}
    for y, row in enumerate(grid):
        for x, col in enumerate(row):
            if col:
                graph[(x, y)] = graph.get((x, y), []) + get_next_nodes(x, y)
    return graph


CHUNKS = {}