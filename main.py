import Map
import pygame
from random import randint

if '__main__' == __name__:
    pygame.init()
    pygame.display.set_caption('Генератор мира')
    # SID = [randint(40, 60), randint(30, 90), randint(70, 90)]
    SID = [40, 60, 80]
    # 1280 720
    lines, columns = Map.NUM_OF_CELLS_CHUNK * 3, Map.NUM_OF_CELLS_CHUNK * 3
    cell_size = 4
    size = width, height = columns * cell_size, lines * cell_size
    screen = pygame.display.set_mode(size)
    board = Map.Map(lines, columns, cell_size, SID)
    all_sprites = pygame.sprite.Group()
    fps = 30
    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                SID = [randint(40, 60), randint(30, 90), randint(70, 90)]
                board = Map.Map(lines, columns, cell_size, SID)
        screen.fill((0, 0, 0))
        board.render(screen)
        all_sprites.draw(screen)
        clock.tick(fps)
        pygame.display.flip()
    pygame.quit()
