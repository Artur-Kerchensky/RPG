from map_generation import filling_table, join_table, BIOMS
import pygame
from config.config import NUM_OF_CELLS_CHUNK


class Map:
    def __init__(self, cell_size, sid, start_coord=(0, 0)):
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

        x = int(pos[0] // self.cell_size) - NUM_OF_CELLS_CHUNK // 2
        y = int(pos[1] // self.cell_size) - NUM_OF_CELLS_CHUNK // 2
        check_x, check_y = abs(x) > NUM_OF_CELLS_CHUNK, abs(y) > NUM_OF_CELLS_CHUNK
        if check_x or check_y:
            self.chunk_update(x, y)
            if check_x:
                return [pos[0] - NUM_OF_CELLS_CHUNK * self.cell_size if x > NUM_OF_CELLS_CHUNK
                        else pos[0] + NUM_OF_CELLS_CHUNK * self.cell_size, pos[1]]
            else:
                return [pos[0], pos[1] - NUM_OF_CELLS_CHUNK * self.cell_size if y > NUM_OF_CELLS_CHUNK
                        else pos[1] + NUM_OF_CELLS_CHUNK * self.cell_size]

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

    def chunk_update(self, x, y):
        if abs(x) > NUM_OF_CELLS_CHUNK:
            coof = 0 if x < NUM_OF_CELLS_CHUNK else -1
            for i in range(len(self.chunks)):
                new_chunk = Chunk(self.chunk_id, self.chunks[i][coof].get_coords()[0] - (NUM_OF_CELLS_CHUNK if not coof
                                                                                         else - NUM_OF_CELLS_CHUNK),
                                  self.chunks[i][coof].get_coords()[1], self.sid)
                self.chunks[i] = [new_chunk] + self.chunks[i][:2] if not coof else self.chunks[i][2:] + [new_chunk]
        else:
            #  abs(y) > NUM_OF_CELLS_CHUNK
            new_chunks = [[]]
            coof = 0 if y < NUM_OF_CELLS_CHUNK else -1
            for chunk in self.chunks[coof]:
                new_chunks[0].append(Chunk(self.chunk_id, chunk.get_coords()[0],
                                        chunk.get_coords()[1] - NUM_OF_CELLS_CHUNK if not coof
                                        else chunk.get_coords()[1] + NUM_OF_CELLS_CHUNK, self.sid))
                self.chunk_id += 1
            self.chunks = new_chunks + self.chunks[:2] if not coof\
                else self.chunks[:2] + new_chunks
        self.loading_map()


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


CHUNKS = {}
