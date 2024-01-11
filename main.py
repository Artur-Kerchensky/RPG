import pygame
from map import Map
from random import randint
from config.config import NUM_OF_CELLS_CHUNK, cell_size
from object import Player


if __name__ == '__main__':
    pygame.init()

    FPS = 60
    WIDTH = 700
    HEIGHT = 394

    pygame.init()
    clock = pygame.time.Clock()
    start_x, start_y = -542, 10 ** 3
    player = Player([start_x, start_y], (100, 100))
    SID = [40, 60, 80]
    size = [NUM_OF_CELLS_CHUNK * cell_size] * 2
    screen = pygame.display.set_mode(size)
    board = Map(cell_size, SID, (start_x, start_y))
    all_sprites = pygame.sprite.Group()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                SID = [randint(40, 60), randint(30, 90), randint(70, 90)]
                start_x, start_y = randint(-10**3, 10**3), randint(NUM_OF_CELLS_CHUNK * 3, 10**3)
                player = Player([start_x, start_y], (100, 100))
                board = Map(cell_size, SID, (start_x, start_y))
            if event.type == pygame.KEYDOWN:
                key_move = {pygame.K_RIGHT: "East", pygame.K_LEFT: 'West',
                            pygame.K_DOWN: 'South', pygame.K_UP: 'North'}
                if event.key in key_move:
                    player.move(key_move[event.key])
        screen.fill((0, 0, 0))
        """На данный момент прогрузка карты не работает"""
        player.change_pos(board.render(screen, player.get_pos_table()))
        player.update(screen)
        all_sprites.draw(screen)
        clock.tick(FPS)
        pygame.display.flip()
    pygame.quit()
