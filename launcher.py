import pygame
import os
import sys

def blitter(*args):
    components = [elem for elem in args]
    if len(components) == 7:
        screen.blit(components[0], (0, 0))
        screen.blit(components[1], (320, 168))
        screen.blit(components[2], (299, 210))
        screen.blit(components[3], (295, 253))
        screen.blit(components[4], (319, 297))
        screen.blit(components[5], (115, 70))
        screen.blit(components[5], (117, 72))
        screen.blit(components[6], (116, 71))
    else:
        screen.blit(components[0], (0, 0))
        screen.blit(components[7], (305, 160))
        screen.blit(components[1], (327, 196))
        screen.blit(components[2], (313, 230))
        screen.blit(components[3], (310, 265))
        screen.blit(components[4], (326, 300))
        screen.blit(components[5], (115, 70))
        screen.blit(components[5], (117, 72))
        screen.blit(components[6], (116, 71))


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
    load_config()
    data["anySaves"] = 0 # Для переключения режима присутствия/отсутствия сохранений (пока)
    font = pygame.font.SysFont('monotypecorsiva', 64)
    title = font.render('The Forgotten Lands', True, (211, 175, 115))
    title_wrap = font.render('The Forgotten Lands', True, (0, 0, 0))
    
    font = pygame.font.SysFont('monotypecorsiva', 30)
    yes = font.render('Да', True, (63, 52, 39))
    no = font.render('Нет', True, (63, 52, 39))
    yes_wrap = font.render('Да', True, (183, 152, 100))
    no_wrap = font.render('Нет', True, (183, 152, 100))
    
    font = pygame.font.SysFont('monotypecorsiva', 20)
    question = font.render('Вы действительно хотите выйти?', True, (63, 52, 39))
    
    if not data["anySaves"]:
        font = pygame.font.SysFont('monotypecorsiva', 24)
        new = font.render('Новая', True, (63, 52, 39))
        load = font.render('Загрузить', True, (63, 52, 39))
        settings = font.render('Настройки', True, (63, 52, 39))
        ex = font.render('Выход', True, (63, 52, 39))
        cont_wrap = font.render('Продолжить', True, (183, 152, 100))
        new_wrap = font.render('Новая', True, (183, 152, 100))
        load_wrap = font.render('Загрузить', True, (183, 152, 100))
        settings_wrap = font.render('Настройки', True, (183, 152, 100))
        ex_wrap = font.render('Выход', True, (183, 152, 100))
        
        background = pygame.transform.scale(load_image('background_no_saves.jpg'), (WIDTH, HEIGHT))
        access_flag = True
        load_flag = False
        settings_flag = False
        exit_flag = False
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                x_pos, y_pos = pygame.mouse.get_pos()
                if 307 < x_pos < 391 and 162 < y_pos < 197 and access_flag:
                    screen.blit(new, (320, 168))
                    screen.blit(new_wrap, (320, 168))
                elif 282 < x_pos < 416 and 205 < y_pos < 240 and access_flag:
                    screen.blit(load, (299, 210))
                    screen.blit(load_wrap, (299, 210))
                elif 276 < x_pos < 423 and 248 < y_pos < 283 and access_flag:
                    screen.blit(settings, (295, 253))
                    screen.blit(settings_wrap, (295, 253))
                elif 307 < x_pos < 391 and 291 < y_pos < 326 and access_flag:
                    screen.blit(ex, (319, 297))
                    screen.blit(ex_wrap, (319, 297))
                elif access_flag:
                    blitter(background, new, load, settings, ex, title_wrap, title)
                if 250 < x_pos < 286 and 200 < y_pos < 233 and exit_flag:
                    context_menu = pygame.transform.scale(load_image("context_menu.png"), (WIDTH // 1.9, HEIGHT // 5.1))
                    screen.blit(context_menu, (175, 165))
                    screen.blit(question, (230, 175))
                    screen.blit(yes, (250, 200))
                    screen.blit(no, (410, 200))
                    screen.blit(yes_wrap, (250, 200))
                if 410 < x_pos < 461 and 200 < y_pos < 233 and exit_flag:
                    context_menu = pygame.transform.scale(load_image("context_menu.png"), (WIDTH // 1.9, HEIGHT // 5.1))
                    screen.blit(context_menu, (175, 165))
                    screen.blit(question, (230, 175))
                    screen.blit(yes, (250, 200))
                    screen.blit(no, (410, 200))
                    screen.blit(no_wrap, (410, 200))
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if 282 < x_pos < 416 and 205 < y_pos < 240 and access_flag:
                        access_flag = False
                        load_flag = True
                        context_menu = pygame.transform.scale(load_image("context_menu.png"), (WIDTH // 1.5, HEIGHT // 1.5))
                        screen.blit(context_menu, (120, 70))
                    elif 276 < x_pos < 423 and 248 < y_pos < 283 and access_flag:
                        access_flag = False
                        settings_flag = True
                        context_menu = pygame.transform.scale(load_image("context_menu.png"), (WIDTH // 1.5, HEIGHT // 1.5))
                        screen.blit(context_menu, (120, 70))
                    elif 307 < x_pos < 391 and 291 < y_pos < 326 and access_flag:
                        access_flag = False
                        exit_flag = True
                        context_menu = pygame.transform.scale(load_image("context_menu.png"), (WIDTH // 1.9, HEIGHT // 5.1))
                        screen.blit(context_menu, (175, 165))
                        screen.blit(question, (230, 175))
                        screen.blit(yes, (250, 200))
                        screen.blit(no, (410, 200))
                    elif 250 < x_pos < 286 and 200 < y_pos < 233 and exit_flag:
                        pygame.quit()
                        sys.exit()
                    elif 410 < x_pos < 461 and 200 < y_pos < 233 and exit_flag:
                        access_flag = True
                        exit_flag = False
                        continue
                    elif not access_flag:
                        if (not (120 < x_pos < 586) or not (70 < y_pos < 332)) and settings_flag and not exit_flag:
                            access_flag = True
                            settings_flag = False
                            continue
                        if (not (120 < x_pos < 586) or not (70 < y_pos < 332)) and load_flag and not exit_flag:
                            access_flag = True
                            load_flag = False
                            continue
                        if (not (175 < x_pos < 543) or not (165 < y_pos < 242)) and exit_flag:
                            access_flag = True
                            exit_flag = False
                            continue
            pygame.display.flip()
            clock.tick(FPS)
    else:
        font = pygame.font.SysFont('monotypecorsiva', 18)
        cont = font.render('Продолжить', True, (63, 52, 39))
        new = font.render('Новая', True, (63, 52, 39))
        load = font.render('Загрузить', True, (63, 52, 39))
        settings = font.render('Настройки', True, (63, 52, 39))
        ex = font.render('Выход', True, (63, 52, 39))
        cont_wrap = font.render('Продолжить', True, (183, 152, 100))
        new_wrap = font.render('Новая', True, (183, 152, 100))
        load_wrap = font.render('Загрузить', True, (183, 152, 100))
        settings_wrap = font.render('Настройки', True, (183, 152, 100))
        ex_wrap = font.render('Выход', True, (183, 152, 100))
        
        background = pygame.transform.scale(load_image('background_saves.jpg'), (WIDTH, HEIGHT))
        access_flag = True
        load_flag = False
        settings_flag = False
        exit_flag = False
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                x_pos, y_pos = pygame.mouse.get_pos()
                if 288 < x_pos < 412 and 157 < y_pos < 184 and access_flag:
                    screen.blit(cont, (305, 160))
                    screen.blit(cont_wrap, (305, 160))
                elif 316 < x_pos < 381 and 192 < y_pos < 219 and access_flag:
                    screen.blit(new, (327, 196))
                    screen.blit(new_wrap, (327, 196))
                elif 299 < x_pos < 401 and 227 < y_pos < 254 and access_flag:
                    screen.blit(load, (313, 230))
                    screen.blit(load_wrap, (313, 230))
                elif 294 < x_pos < 405 and 262 < y_pos < 289 and access_flag:
                    screen.blit(settings, (310, 265))
                    screen.blit(settings_wrap, (310, 265))
                elif 316 < x_pos < 383 and 297 < y_pos < 324 and access_flag:
                    screen.blit(ex, (326, 300))
                    screen.blit(ex_wrap, (326, 300))
                elif access_flag:
                    blitter(background, new, load, settings, ex, title_wrap, title, cont)
                if 250 < x_pos < 286 and 200 < y_pos < 233 and exit_flag:
                    context_menu = pygame.transform.scale(load_image("context_menu.png"), (WIDTH // 1.9, HEIGHT // 5.1))
                    screen.blit(context_menu, (175, 165))
                    screen.blit(question, (230, 175))
                    screen.blit(yes, (250, 200))
                    screen.blit(no, (410, 200))
                    screen.blit(yes_wrap, (250, 200))
                if 410 < x_pos < 461 and 200 < y_pos < 233 and exit_flag:
                    context_menu = pygame.transform.scale(load_image("context_menu.png"), (WIDTH // 1.9, HEIGHT // 5.1))
                    screen.blit(context_menu, (175, 165))
                    screen.blit(question, (230, 175))
                    screen.blit(yes, (250, 200))
                    screen.blit(no, (410, 200))
                    screen.blit(no_wrap, (410, 200))
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if 299 < x_pos < 401 and 227 < y_pos < 254 and access_flag:
                        access_flag = False
                        load_flag = True
                        context_menu = pygame.transform.scale(load_image("context_menu.png"), (WIDTH // 1.5, HEIGHT // 1.5))
                        screen.blit(context_menu, (120, 70))
                    elif 276 < x_pos < 423 and 248 < y_pos < 283 and access_flag:
                        access_flag = False
                        settings_flag = True
                        context_menu = pygame.transform.scale(load_image("context_menu.png"), (WIDTH // 1.5, HEIGHT // 1.5))
                        screen.blit(context_menu, (120, 70))
                    elif 307 < x_pos < 391 and 291 < y_pos < 326 and access_flag:
                        access_flag = False
                        exit_flag = True
                        context_menu = pygame.transform.scale(load_image("context_menu.png"), (WIDTH // 1.9, HEIGHT // 5.1))
                        screen.blit(context_menu, (175, 165))
                        screen.blit(question, (230, 175))
                        screen.blit(yes, (250, 200))
                        screen.blit(no, (410, 200))
                    elif 250 < x_pos < 286 and 200 < y_pos < 233 and exit_flag:
                        pygame.quit()
                        sys.exit()
                    elif 410 < x_pos < 461 and 200 < y_pos < 233 and exit_flag:
                        access_flag = True
                        exit_flag = False
                        continue
                    elif not access_flag:
                        if (not (120 < x_pos < 586) or not (70 < y_pos < 332)) and settings_flag and not exit_flag:
                            access_flag = True
                            settings_flag = False
                            continue
                        if (not (120 < x_pos < 586) or not (70 < y_pos < 332)) and load_flag and not exit_flag:
                            access_flag = True
                            load_flag = False
                            continue
                        if (not (175 < x_pos < 543) or not (165 < y_pos < 242)) and exit_flag:
                            access_flag = True
                            exit_flag = False
                            continue
            pygame.display.flip()
            clock.tick(FPS)


def load_config():
    global data
    filename = os.path.join('config', "cfg.txt")
    with open(filename, "r+") as config:
        raw_data = config.read()[:-1]
        if not raw_data:
            config.write("resolutionWidth=1280\n")
            config.write("resolutionHeight=720\n")
            config.write("anySaves=0\n")
            config.write("difficult=1\n")
        else:
            data = {item.split("=")[0]: int(item.split("=")[1]) for item in raw_data.split("\n")}          

            
if __name__ == '__main__':
    pygame.init()
    FPS = 60
    WIDTH = 700
    HEIGHT = 394

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT), flags=pygame.NOFRAME)
    clock = pygame.time.Clock()
    start_screen()