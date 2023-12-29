from map import Map, NUM_OF_CELLS_CHUNK
import pygame
from random import randint

if '__main__' == __name__:
    pygame.init()
    pygame.display.set_caption('Генератор мира')
    # SID = [randint(40, 60), randint(30, 90), randint(70, 90)]
    start_x, start_y = 0, 0
    SID = [40, 60, 80]
    cell_size = 12
    size = [NUM_OF_CELLS_CHUNK * 3 * cell_size] * 2
    screen = pygame.display.set_mode(size)
    board = Map(cell_size, SID, (start_x, start_y))

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
                start_x, start_y = randint(64, 1000), randint(64, 1000)
                board = Map(cell_size, SID, (start_x, start_y))
        screen.fill((0, 0, 0))
        board.render(screen)
        all_sprites.draw(screen)
        clock.tick(fps)
        pygame.display.flip()
    pygame.quit()
