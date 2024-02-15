import pygame
from map import Map, Camera
from random import randint
from config.config import NUM_OF_CELLS_CHUNK, cell_size
from object import Player, Enemy


if __name__ == '__main__':
    pygame.init()
    FPS = 60
    WIDTH = 700
    HEIGHT = 394
    pygame.init()
    clock = pygame.time.Clock()
    pos = [randint(1000, 10**6), randint(1000, 10**6)]
    enemies = [Enemy('Утка', [pos[0] + 2, pos[1] + 2], (100, 100), 100)]
    player = Player(pos, (100, 100))
    SID = [60, 70, 80]
    size = [NUM_OF_CELLS_CHUNK * cell_size] * 2
    screen = pygame.display.set_mode(size)
    board = Map(SID, pos)
    camera = Camera(board)
    all_sprites = pygame.sprite.Group()
    running = True
    moving = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:

                SID = [randint(40, 60), randint(30, 90), randint(70, 90)]
                start_x, start_y = randint(-10**3, 10**3), randint(NUM_OF_CELLS_CHUNK * 3, 10**3)
                player = Player([start_x, start_y], (100, 100))
                board = Map(SID, (start_x, start_y))
                camera = Camera(board)

            if event.type == pygame.KEYDOWN:
                key_move = {pygame.K_RIGHT: "East", pygame.K_LEFT: 'West',
                            pygame.K_DOWN: 'South', pygame.K_UP: 'North'}
                if event.key in key_move:
                    player.move(key_move[event.key])
                    moving = True
                    pos = player.get_pos()
                    camera.move(key_move[event.key])

        for enemy_list in board.get_enemy():
            if enemy_list:
                for enemy in enemy_list:
                    if enemy not in enemies:
                        enemies.append(enemy)

        screen.fill((0, 0, 0))
        board.render(screen, camera.get_pos())
        player.update(screen)
        [enemy.update(screen, pos, board, moving) for enemy in enemies]
        moving = False
        player.update(screen)
        clock.tick(FPS)
        pygame.display.flip()
    pygame.quit()
