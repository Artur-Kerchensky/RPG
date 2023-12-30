from map_generation import filling_table, join_table, BIOMS
import pygame


NUM_OF_CELLS_CHUNK = 21


class Map:
    def __init__(self, cell_size, sid, start_coord=(0, 0),  load_chunk=1):
        self.size = NUM_OF_CELLS_CHUNK * 3
        self.cell_size = cell_size
        self.start_x, self.start_y = start_coord[0], start_coord[1]
        self.x_start_chunk, self.y_start_chunk = self.start_x // NUM_OF_CELLS_CHUNK, self.start_y // NUM_OF_CELLS_CHUNK
        self.chunks = []
        self.board = []
        for i in range(self.x_start_chunk, 3 + self.x_start_chunk):
            for j in range(self.y_start_chunk, 3 + self.y_start_chunk):
                self.chunks.append(Chunk(i, -NUM_OF_CELLS_CHUNK + NUM_OF_CELLS_CHUNK * j,
                                         -NUM_OF_CELLS_CHUNK + NUM_OF_CELLS_CHUNK * i, sid))
        for i in range(3):
            self.board.append(join_table(list(i.get_chunk() for i in self.chunks[3 * i:3 * (i + 1)])))
        self.board = join_table(self.board, direction='height')

    def render(self, screen):
        for height in range(self.size):
            for width in range(self.size):
                left, top = width * self.cell_size, height * self.cell_size
                color = BIOMS[self.board[height][width]].get_color()
                pygame.draw.rect(screen, pygame.Color(color), [left, top, self.cell_size, self.cell_size])


class Chunk:
    def __init__(self, id, x, y, sid):
        self.id = id
        self.x, self.y = x, y
        self.num = NUM_OF_CELLS_CHUNK
        self.table = filling_table(x, y, self.num, self.num, sid)

    def get_chunk(self):
        return self.table

    def get_coord(self):
        return self.x, self.y

    def get_id(self):
        return self.id


CHUNKS = {}
