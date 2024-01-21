import pygame
from map_generation import filling_table, join_table, BIOMS
from config.config import NUM_OF_CELLS_CHUNK, cell_size


class Map:
    def __init__(self, sid, start_coord=(0, 0)):
        self.size = NUM_OF_CELLS_CHUNK * 3
        self.cell_size = cell_size
        self.start_x, self.start_y = start_coord[0], start_coord[1]
        self.sid = sid
        self.chunk_id = 0
        self.chunks = []
        self.board = []
        for i in [-3, -1, 1]:
            self.chunks.append([])
            for j in [-3, -1, 1]:
                self.chunks[-1].append(Chunk(self.chunk_id, (2 * self.start_x + NUM_OF_CELLS_CHUNK * j) // 2,
                                             (2 * self.start_y + NUM_OF_CELLS_CHUNK * i) // 2, self.sid))
                self.chunk_id += 1
        self.loading_map()

    def render(self, screen, pos):
        x = pos[0]
        y = pos[1]
        for height in range(NUM_OF_CELLS_CHUNK + y, NUM_OF_CELLS_CHUNK * 2 + y):
            for width in range(NUM_OF_CELLS_CHUNK + x, NUM_OF_CELLS_CHUNK * 2 + x):
                left = (width - NUM_OF_CELLS_CHUNK - x) * self.cell_size
                top = (height - NUM_OF_CELLS_CHUNK - y) * self.cell_size
                color = BIOMS[self.board[height][width]].get_color()
                pygame.draw.rect(screen, pygame.Color(color), [left, top, self.cell_size, self.cell_size])

    def loading_map(self):
        self.board = []
        for list_chunks in self.chunks:
            self.board.append(join_table(list(chunk.get_chunk() for chunk in list_chunks)))

        self.board = join_table(self.board, direction='height')

    def chunk_update(self, pos):
        x, y = pos[0], pos[1]
        if abs(x) > NUM_OF_CELLS_CHUNK // 2:
            coof = 0 if x < NUM_OF_CELLS_CHUNK // 2 else -1
            for i in range(len(self.chunks)):
                new_chunk = Chunk(self.chunk_id,
                                  self.chunks[i][coof].get_coords()[0] - (NUM_OF_CELLS_CHUNK if not coof
                                                                          else - NUM_OF_CELLS_CHUNK),
                                  self.chunks[i][coof].get_coords()[1], self.sid)
                self.chunks[i] = [new_chunk] + self.chunks[i][:2] if not coof else self.chunks[i][1:] + [new_chunk]
        else:
            #  abs(y) > NUM_OF_CELLS_CHUNK
            new_chunks = [[]]
            coof = 0 if y < NUM_OF_CELLS_CHUNK // 2 else -1

            for chunk in self.chunks[coof]:
                new_chunks[0].append(Chunk(self.chunk_id, chunk.get_coords()[0],
                                           chunk.get_coords()[1] - NUM_OF_CELLS_CHUNK if not coof
                                           else chunk.get_coords()[1] + NUM_OF_CELLS_CHUNK, self.sid))
                self.chunk_id += 1
            self.chunks = new_chunks + self.chunks[:2] if not coof else self.chunks[1:] + new_chunks

        self.loading_map()

    def get_chunks(self):
        return self.chunks

    def get_board(self):
        return self.board


class Chunk:
    def __init__(self, id, x, y, sid):
        self.id = id
        self.x, self.y = x, y
        self.num = NUM_OF_CELLS_CHUNK
        self.table = filling_table(x, y, NUM_OF_CELLS_CHUNK, NUM_OF_CELLS_CHUNK, sid)

    def get_chunk(self):
        return self.table

    def get_coords(self):
        return self.x, self.y

    def get_id(self):
        return self.id


class Camera:
    def __init__(self, map_object):
        self.pos = [0, 0]
        self.map_object = map_object

    def move(self, direction):
        directions = {'North': (0, -1), 'South': (0, 1), 'East': (1, 0), 'West': (-1, 0)}
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

        if abs(self.pos[0]) > NUM_OF_CELLS_CHUNK // 2 or abs(self.pos[1]) > NUM_OF_CELLS_CHUNK // 2:
            raise IndexError(self.pos)
        return self.pos


CHUNKS = {}
