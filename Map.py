from map_generation import filling_table, join_table, BIOMS
import pygame


NUM_OF_CELLS_CHUNK = 64


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
        self.num = NUM_OF_CELLS_CHUNK
        self.table = filling_table(x, y, self.num, self.num, sid)

    def get_chunk(self):
        return self.table

    def get_coord(self):
        return self.x, self.y

    def get_id(self):
        return self.id


CHUNKS = {}
