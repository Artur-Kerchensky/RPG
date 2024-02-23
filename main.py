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
        # pos = 1000, 4000
        # SID = [40, 60, 80]
        player = Player(pos, (100, 100))
        board = Map(SID, pos)
        player.examination(board)
        camera = Camera(board, [pos[0] - player.get_pos()[0], pos[1] - player.get_pos()[1]])
        size = [NUM_OF_CELLS_CHUNK * cell_size] * 2
        screen = pygame.display.set_mode(size)
        direction = "South"
        running = True
        moving = False
        flag = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    key_move = {pygame.K_RIGHT: "East", pygame.K_LEFT: 'West',
                                pygame.K_DOWN: 'South', pygame.K_UP: 'North', pygame.K_s: 'South', pygame.K_w: 'North',
                                pygame.K_d: 'East', pygame.K_a: 'West'}
                    if event.key in key_move:
                        direction = key_move[event.key]
                        moving = player.move(direction, board.get_impenetrable())
                        pos = player.get_pos()
                        camera.move(key_move[event.key], moving)
                        flag = True

            for enemy_list in board.get_enemy():
                if enemy_list:
                    for enemy in enemy_list:
                        if enemy not in enemies:
                            enemies.append(enemy)

            if flag:
                screen.fill((0, 0, 0))
                board.render(screen, camera.get_pos())
                [enemy.update(screen, pos, board, moving) for enemy in enemies]
                moving = False
                player.render(screen, direction)
                flag = False
            clock.tick(FPS)
            pygame.display.flip()
        pygame.quit()
