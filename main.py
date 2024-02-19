import pygame
from map import Map, Camera
from random import randint
from configuration import NUM_OF_CELLS_CHUNK, cell_size, load_image
from object import Player
from launcher import start_screen


if __name__ == '__main__':
    pygame.init()
    if start_screen():
        pygame.init()
        pygame.display.set_caption('The Forgotten Lands')
        pygame.display.set_icon(load_image("icon.png", "menu"))
        FPS = 30
        WIDTH = 700
        HEIGHT = 394
        pygame.init()
        clock = pygame.time.Clock()
        all_sprites = pygame.sprite.Group()
        enemies = []
        SID = [randint(40, 60), randint(30, 90), randint(70, 90)]
        pos = [randint(1000, 10**6), randint(1000, 10**6)]
        player = Player(pos, (100, 100))
        board = Map(SID, pos)
        camera = Camera(board)
        size = [NUM_OF_CELLS_CHUNK * cell_size] * 2
        screen = pygame.display.set_mode(size)
        direction = "South"
        running = True
        moving = False
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    key_move = {pygame.K_RIGHT: "East", pygame.K_LEFT: 'West',
                                pygame.K_DOWN: 'South', pygame.K_UP: 'North'}
                    if event.key in key_move:

                        direction = key_move[event.key]
                        player.move(direction)
                        player.update(screen, direction)
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
            [enemy.update(screen, pos, board, moving) for enemy in enemies]
            moving = False
            player.render(screen, direction)
            clock.tick(FPS)
            pygame.display.flip()
        pygame.quit()