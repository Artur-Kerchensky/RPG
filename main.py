import pygame
import os
import sys


def load_image(name, colorkey=None):
    fullname = os.path.join('menu', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load("menu/" + name)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image

def start_screen():
    background = pygame.transform.scale(load_image('background.jpg'), (WIDTH, HEIGHT))
    button1 = load_image('button1.png')
    button1_active = pygame.transform.scale(button1, (110, 50))
    button2 = load_image('button2.png')
    button2_active = pygame.transform.scale(button2, (166, 50))
    button3 = load_image('button3.png')
    button3_active = pygame.transform.scale(button3, (178, 50))
    button4 = load_image('button4.png')
    button4_active = pygame.transform.scale(button4, (110, 50))
    screen.blit(background, (0, 0))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            x_pos, y_pos = pygame.mouse.get_pos()
            if 307 <= x_pos <= 391 and 162 <= y_pos <= 197:
                screen.blit(button1_active, (300, 155))
            elif 282 <= x_pos <= 416 and 205 <= y_pos <= 240:
                screen.blit(button2_active, (275, 198))
            elif 276 <= x_pos <= 423 and 248 <= y_pos <= 283:
                screen.blit(button3_active, (269, 241))
            elif 307 <= x_pos <= 391 and 291 <= y_pos <= 326:
                screen.blit(button4_active, (300, 284))
            else:
                screen.blit(background, (0, 0))
                screen.blit(button1, (307, 162))
                screen.blit(button2, (282, 205))
                screen.blit(button3, (276, 248))
                screen.blit(button4, (307, 291))
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 307 <= x_pos <= 391 and 291 <= y_pos <= 326:
                    pygame.quit()
        pygame.display.flip()
        clock.tick(FPS)

if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Меню <3')
    FPS = 60
    WIDTH = 700
    HEIGHT = 394

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT), flags=pygame.NOFRAME)
    clock = pygame.time.Clock()
    start_screen()