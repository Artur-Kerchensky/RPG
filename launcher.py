import os
import sys
import pygame
from configuration import load_config, load_image

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


def blitter_load(*args):
    components = [elem for elem in args]
    if len(components) == 2:
        screen.blit(components[0], (120, 70))
        [screen.blit(components[1], (325, 130 + 60 * i)) for i in range(3)]
        [screen.fill((63, 52, 39), (182, 110 + 60 * i, 330 + 5 * i, 2)) for i in range(4)]
    else:
        screen.blit(components[0], (120, 70))
        epic_1 = pygame.font.SysFont('monotypecorsiva', 56).render('В разработке', True, (63, 52, 39))
        epic_2 = pygame.transform.rotate(epic_1, -22.5)
        screen.blit(epic_2, (210, 110))
        

def blitter_settings(*args):
    components = [elem for elem in args]
    screen.blit(components[0], (120, 70))
    screen.blit(components[1], (180, 90))
    screen.blit(components[2], (180, 120))
    screen.blit(components[3], (400, 120))
    screen.blit(components[4], (180, 170))
    screen.blit(components[5], (180, 200))
    screen.blit(components[6], (290, 200))
    screen.blit(components[7], (400, 200))
    screen.blit(components[8], (245, 250))
    screen.blit(components[9], (485, 240))
    screen.blit(components[10], (215, 235))


def blitter_exit(*args):
    components = [elem for elem in args]
    screen.blit(components[0], (175, 165))
    screen.blit(components[1], (230, 175))
    screen.blit(components[2], (250, 200))
    screen.blit(components[3], (410, 200))

def play_music():
    data = load_config()
    pygame.mixer.music.load("data/music/menu.mp3")
    pygame.mixer.music.set_volume(data["volume"]/100)
    pygame.mixer.music.play(-1)


def start_screen():
    data = load_config()
    play_music()
    font = pygame.font.SysFont('monotypecorsiva', 64)
    title = font.render('The Forgotten Lands', True, (211, 175, 115))
    title_wrap = font.render('The Forgotten Lands', True, (0, 0, 0))
    temp_volume = data["volume"]
    
    font = pygame.font.SysFont('monotypecorsiva', 48)
    vol_option1 =  font.render('+', True, (63, 52, 39))
    vol_option2 =  font.render('-', True, (63, 52, 39))
    vol_option1_wrap =  font.render('+', True, (183, 152, 100))
    vol_option2_wrap =  font.render('-', True, (183, 152, 100))
    
    font = pygame.font.SysFont('monotypecorsiva', 30)
    yes = font.render('Да', True, (63, 52, 39))
    no = font.render('Нет', True, (63, 52, 39))
    res_option1 = font.render('1920x1080', True, (63, 52, 39))
    res_option2 = font.render('1280x720', True, (63, 52, 39))
    dif_option1 = font.render('Легкий', True, (63, 52, 39))
    dif_option2 = font.render('Средний', True, (63, 52, 39))
    dif_option3 = font.render('Сложный', True, (63, 52, 39))
    yes_wrap = font.render('Да', True, (183, 152, 100))
    no_wrap = font.render('Нет', True, (183, 152, 100))
    res_option1_wrap = font.render('1920x1080', True, (183, 152, 100))
    res_option2_wrap = font.render('1280x720', True, (183, 152, 100))
    dif_option1_wrap = font.render('Легкий', True, (183, 152, 100))
    dif_option2_wrap = font.render('Средний', True, (183, 152, 100))
    dif_option3_wrap = font.render('Сложный', True, (183, 152, 100))
    
    font = pygame.font.SysFont('monotypecorsiva', 24)
    settings_res = font.render('Разрешение экрана:', True, (63, 52, 39))
    settings_dif = font.render('Уровень сложности:', True, (63, 52, 39))
    settings_vol = font.render(f'Громкость музыки ({data["volume"]}%)', True, (63, 52, 39))
    empty = font.render('Пусто', True, (63, 52, 39))
    empty_wrap = font.render('Пусто', True, (183, 152, 100))
    
    font = pygame.font.SysFont('monotypecorsiva', 20)
    question = font.render('Вы действительно хотите выйти?', True, (63, 52, 39))
    
    font = pygame.font.SysFont('monotypecorsiva', 16)
    warning = font.render('Изменения вступят в силу после перезапуска игры', True, (63, 52, 39))
    
    medium_context_menu = pygame.transform.scale(load_image("context_menu.png", "menu"), (WIDTH // 1.5, HEIGHT // 1.5))
    small_context_menu = pygame.transform.scale(load_image("context_menu.png", "menu"), (WIDTH // 1.9, HEIGHT // 5.1))
    

    
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
        
        
        background = pygame.transform.scale(load_image('background_no_saves.jpg', "menu"), (WIDTH, HEIGHT))
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
                
                if 325 < x_pos < 385 and 130 < y_pos < 157 and load_flag:
                    blitter_load(medium_context_menu, empty)
                    screen.blit(empty_wrap, (325, 130))
                elif 325 < x_pos < 385 and 190 < y_pos < 217 and load_flag:
                    blitter_load(medium_context_menu, empty)
                    screen.blit(empty_wrap, (325, 190))
                elif 325 < x_pos < 385 and 250 < y_pos < 277 and load_flag:
                    blitter_load(medium_context_menu, empty)
                    screen.blit(empty_wrap, (325, 250))
                elif load_flag:
                    blitter_load(medium_context_menu, empty)


                if 180 < x_pos < 299 and 130 < y_pos < 163 and settings_flag:
                    blitter_settings(medium_context_menu, settings_res, res_option1, res_option2, settings_dif,
                                     dif_option1, dif_option2, dif_option3, settings_vol, vol_option1, vol_option2)
                    screen.blit(res_option1_wrap, (180, 120))
                    screen.blit(warning, (210, 290))
                elif 400 < x_pos < 506 and 130 < y_pos < 163 and settings_flag:
                    blitter_settings(medium_context_menu, settings_res, res_option1, res_option2, settings_dif,
                                     dif_option1, dif_option2, dif_option3, settings_vol, vol_option1, vol_option2)
                    screen.blit(res_option2_wrap, (400, 120))
                    screen.blit(warning, (210, 290))
                elif 180 < x_pos < 264 and 210 < y_pos < 243 and settings_flag:
                    blitter_settings(medium_context_menu, settings_res, res_option1, res_option2, settings_dif,
                                     dif_option1, dif_option2, dif_option3, settings_vol, vol_option1, vol_option2)
                    screen.blit(dif_option1_wrap, (180, 200))
                    screen.blit(warning, (210, 290))
                elif 290 < x_pos < 385 and 210 < y_pos < 243 and settings_flag:
                    blitter_settings(medium_context_menu, settings_res, res_option1, res_option2, settings_dif,
                                     dif_option1, dif_option2, dif_option3, settings_vol, vol_option1, vol_option2)
                    screen.blit(dif_option2_wrap, (290, 200))
                    screen.blit(warning, (210, 290))
                elif 400 < x_pos < 509 and 210 < y_pos < 243 and settings_flag:
                    blitter_settings(medium_context_menu, settings_res, res_option1, res_option2, settings_dif,
                                     dif_option1, dif_option2, dif_option3, settings_vol, vol_option1, vol_option2)
                    screen.blit(dif_option3_wrap, (400, 200))
                    screen.blit(warning, (210, 290))
                elif 485 < x_pos < 513 and 240 < y_pos < 293 and settings_flag:
                    blitter_settings(medium_context_menu, settings_res, res_option1, res_option2, settings_dif,
                                     dif_option1, dif_option2, dif_option3, settings_vol, vol_option1, vol_option2)
                    screen.blit(vol_option1_wrap, (485, 240))
                    screen.blit(warning, (210, 290))
                elif 215 < x_pos < 231 and 235 < y_pos < 288 and settings_flag:
                    blitter_settings(medium_context_menu, settings_res, res_option1, res_option2, settings_dif,
                                     dif_option1, dif_option2, dif_option3, settings_vol, vol_option1, vol_option2)
                    screen.blit(vol_option2_wrap, (215, 235))
                    screen.blit(warning, (210, 290))
                elif settings_flag:
                    blitter_settings(medium_context_menu, settings_res, res_option1, res_option2, settings_dif,
                                     dif_option1, dif_option2, dif_option3, settings_vol, vol_option1, vol_option2)


                if 250 < x_pos < 286 and 200 < y_pos < 233 and exit_flag:
                    blitter_exit(small_context_menu, question, yes, no)
                    screen.blit(yes_wrap, (250, 200))
                elif 410 < x_pos < 461 and 200 < y_pos < 233 and exit_flag:
                    blitter_exit(small_context_menu, question, yes, no)
                    screen.blit(no_wrap, (410, 200))
                elif exit_flag:
                    blitter_exit(small_context_menu, question, yes, no)


                if event.type == pygame.MOUSEBUTTONDOWN:
                    if 307 < x_pos < 391 and 162 < y_pos < 197 and access_flag:
                        pygame.mixer.music.pause()
                        return True
                    if 282 < x_pos < 416 and 205 < y_pos < 240 and access_flag:
                        access_flag = False
                        load_flag = True
                        blitter_load(medium_context_menu, empty)
                    elif 276 < x_pos < 423 and 248 < y_pos < 283 and access_flag:
                        access_flag = False
                        settings_flag = True
                        blitter_settings(medium_context_menu, settings_res, res_option1, res_option2, settings_dif,
                                         dif_option1, dif_option2, dif_option3, settings_vol, vol_option1, vol_option2)
                    elif 180 < x_pos < 299 and 130 < y_pos < 163 and settings_flag:
                        load_config((1920, 1080), "res")
                    elif 400 < x_pos < 506 and 130 < y_pos < 163 and settings_flag:
                        load_config((1280, 720), "res")
                    elif 180 < x_pos < 264 and 210 < y_pos < 243 and settings_flag:
                        load_config(0, "dif")
                    elif 290 < x_pos < 385 and 210 < y_pos < 243 and settings_flag:
                        load_config(1, "dif")
                    elif 400 < x_pos < 509 and 210 < y_pos < 243 and settings_flag:
                        load_config(2, "dif")
                    elif 307 < x_pos < 391 and 291 < y_pos < 326 and access_flag:
                        access_flag = False
                        exit_flag = True
                        blitter_exit(small_context_menu, question, yes, no)
                    elif 250 < x_pos < 286 and 200 < y_pos < 233 and exit_flag:
                        pygame.mixer.music.pause()
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
        
        background = pygame.transform.scale(load_image('background_saves.jpg', "menu"), (WIDTH, HEIGHT))
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
                
                
                if 180 < x_pos < 299 and 130 < y_pos < 163 and settings_flag:
                    blitter_settings(medium_context_menu, settings_res, res_option1, res_option2, settings_dif,
                                     dif_option1, dif_option2, dif_option3, settings_vol, vol_option1, vol_option2)
                    screen.blit(res_option1_wrap, (180, 120))
                    screen.blit(warning, (210, 290))
                elif 400 < x_pos < 506 and 130 < y_pos < 163 and settings_flag:
                    blitter_settings(medium_context_menu, settings_res, res_option1, res_option2, settings_dif,
                                     dif_option1, dif_option2, dif_option3, settings_vol, vol_option1, vol_option2)
                    screen.blit(res_option2_wrap, (400, 120))
                    screen.blit(warning, (210, 290))
                elif 180 < x_pos < 264 and 210 < y_pos < 243 and settings_flag:
                    blitter_settings(medium_context_menu, settings_res, res_option1, res_option2, settings_dif,
                                     dif_option1, dif_option2, dif_option3, settings_vol, vol_option1, vol_option2)
                    screen.blit(dif_option1_wrap, (180, 200))
                    screen.blit(warning, (210, 290))
                elif 290 < x_pos < 385 and 210 < y_pos < 243 and settings_flag:
                    blitter_settings(medium_context_menu, settings_res, res_option1, res_option2, settings_dif,
                                     dif_option1, dif_option2, dif_option3, settings_vol, vol_option1, vol_option2)
                    screen.blit(dif_option2_wrap, (290, 200))
                    screen.blit(warning, (210, 290))
                elif 400 < x_pos < 509 and 210 < y_pos < 243 and settings_flag:
                    blitter_settings(medium_context_menu, settings_res, res_option1, res_option2, settings_dif,
                                     dif_option1, dif_option2, dif_option3, settings_vol, vol_option1, vol_option2)
                    screen.blit(dif_option3_wrap, (400, 200))
                    screen.blit(warning, (210, 290))
                elif 485 < x_pos < 513 and 240 < y_pos < 293 and settings_flag:
                    blitter_settings(medium_context_menu, settings_res, res_option1, res_option2, settings_dif,
                                     dif_option1, dif_option2, dif_option3, settings_vol, vol_option1, vol_option2)
                    screen.blit(vol_option1_wrap, (485, 240))
                    screen.blit(warning, (210, 290))
                elif 215 < x_pos < 231 and 235 < y_pos < 288 and settings_flag:
                    blitter_settings(medium_context_menu, settings_res, res_option1, res_option2, settings_dif,
                                     dif_option1, dif_option2, dif_option3, settings_vol, vol_option1, vol_option2)
                    screen.blit(vol_option2_wrap, (215, 235))
                    screen.blit(warning, (210, 290))
                elif settings_flag:
                    blitter_settings(medium_context_menu, settings_res, res_option1, res_option2, settings_dif,
                                     dif_option1, dif_option2, dif_option3, settings_vol, vol_option1, vol_option2)


                if 250 < x_pos < 286 and 200 < y_pos < 233 and exit_flag:
                    blitter_exit(small_context_menu, question, yes, no)
                    screen.blit(yes_wrap, (250, 200))
                elif 410 < x_pos < 461 and 200 < y_pos < 233 and exit_flag:
                    blitter_exit(small_context_menu, question, yes, no)
                    screen.blit(no_wrap, (410, 200))
                elif exit_flag:
                    blitter_exit(small_context_menu, question, yes, no)
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if 288 < x_pos < 412 and 157 < y_pos < 184 and access_flag:
                        pygame.mixer.music.pause()
                        return True
                    elif 316 < x_pos < 381 and 192 < y_pos < 219 and access_flag:
                        pygame.mixer.music.pause()
                        return True
                    elif 299 < x_pos < 401 and 227 < y_pos < 254 and access_flag:
                        access_flag = False
                        load_flag = True
                        blitter_load(medium_context_menu)
                    elif 276 < x_pos < 423 and 248 < y_pos < 283 and access_flag:
                        access_flag = False
                        settings_flag = True
                        screen.blit(medium_context_menu, (120, 70))
                    elif 180 < x_pos < 299 and 130 < y_pos < 163 and settings_flag:
                        load_config((1920, 1080), "res")
                    elif 400 < x_pos < 506 and 130 < y_pos < 163 and settings_flag:
                        load_config((1280, 720), "res")
                    elif 180 < x_pos < 264 and 210 < y_pos < 243 and settings_flag:
                        load_config(0, "dif")
                    elif 290 < x_pos < 385 and 210 < y_pos < 243 and settings_flag:
                        load_config(1, "dif")
                    elif 400 < x_pos < 509 and 210 < y_pos < 243 and settings_flag:
                        load_config(2, "dif")
                    elif 485 < x_pos < 513 and 240 < y_pos < 293 and settings_flag:
                        temp_volume += 10 
                        load_config(min(temp_volume, 100), "vol")
                    elif 215 < x_pos < 231 and 235 < y_pos < 288 and settings_flag:
                        temp_volume -= 10 
                        load_config(max(temp_volume, 0), "vol")
                    elif 307 < x_pos < 391 and 291 < y_pos < 326 and access_flag:
                        access_flag = False
                        exit_flag = True
                        blitter_exit(small_context_menu, question, yes, no)
                    elif 250 < x_pos < 286 and 200 < y_pos < 233 and exit_flag:
                        pygame.mixer.music.pause()
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
    


FPS = 60
WIDTH = 700
HEIGHT = 394
screen = pygame.display.set_mode((WIDTH, HEIGHT), flags=pygame.NOFRAME)
pygame.display.set_caption('The Forgotten Lands')
pygame.display.set_icon(load_image("icon.jpg", "menu"))
clock = pygame.time.Clock()
    

if __name__ == '__main__':
    pygame.init()
    start_screen()