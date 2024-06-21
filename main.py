
from PIL import Image
import time
import pygame
from game2 import *
from random import randint


pygame.init()
width, height = 1024, 280
resolution = (width, height)
window = pygame.display.set_mode(resolution)

speed = 8.3 #8.3
money = 300
score_music = 0 #co sto


dino_menu = True #default

naruto_menu = False
naruto_locked = True

pika_menu = False
pika_locked = True

Dino_xy = [70, 190]

dino = Dino(Dino_xy[0], Dino_xy[1], dino_menu, naruto_menu, pika_menu)
background = Background(width, 240, dino_menu, naruto_menu, pika_menu)
length = HowFar(930, 20)
cactus = Cactus(width, 190, dino_menu, naruto_menu, pika_menu, speed)
game_over = GameOver(390, 100)
cash = Cash(width, 190)

courent_time = time.time()
time_to_see_cactus = 1.5


WHITE = (255, 255, 255)
#definiowe czcinek
font = pygame.font.Font('Font/PressStart2P-Regular.ttf', 16)
pygame.display.set_caption('Main Menu')

hi_score_bool = False
game_paused = False
resume = False
menu_state = "main"

#przyciski menu
start_img = pygame.image.load("Menu/button_start.png").convert_alpha()
change_character_img = pygame.image.load("Menu/button_shop.png").convert_alpha()
quit_img = pygame.image.load("Menu/button_quit.png").convert_alpha()
resume_img = pygame.image.load("Menu/button_resume.png").convert_alpha()
restart_img = pygame.image.load("Menu/button_restart.png").convert_alpha()
restart_img2 = pygame.image.load(f'Menu/Restart/restart_button1.png')
dino_menu_img = pygame.image.load("Menu/button_dino.png").convert_alpha()

naruto_locked_menu_img = pygame.image.load("Menu/button_naruto_locked.png").convert_alpha()
pikachu_locked_menu_img = pygame.image.load("Menu/button_pikachu_locked.png").convert_alpha()

naruto_menu_img = pygame.image.load("Menu/button_naruto.png").convert_alpha()
pikachu_menu_img = pygame.image.load("Menu/button_pikachu.png").convert_alpha()


old_buy_img = pygame.image.load("Menu/button_buy.png")
buy_img = pygame.transform.scale(old_buy_img, (151, 55))

old_buy_img_transparent = pygame.image.load("Menu/button_buy_transparent.png")
buy_img_transparent = pygame.transform.scale(old_buy_img_transparent, (151, 55))

#INSTANCJA PRZYCISKÓW
#Main menu
start_button = Button(40, 100, start_img, 1)
change_button = Button(380, 100, change_character_img, 1) #shop
quit_button = Button(760, 100, quit_img, 1) #zawsze na koncu po prawej stronie
#Rssume manu
resume_button = Button(40, 100, resume_img, 1)
restart_button = Button(380, 100, restart_img, 1)
#Restart button
restart_button2 = Button(485, 135, restart_img2, 1)
#Characters and button buy
dino_button = Button(40, 100, dino_menu_img, 1)

naruto_button = Button(380, 100, naruto_menu_img, 1)
naruto_button_locked = Button(380, 100, naruto_locked_menu_img, 1)
buy_button_naruto = Button(415, 200, buy_img, 1)

pikachu_button = Button(760, 100, pikachu_menu_img, 1)
pikachu_button_locked = Button(760, 100, pikachu_locked_menu_img, 1)
buy_button_pikachu = Button(800, 200, buy_img, 1)

#zmiana przeźroczystości buy
buy_button_naruto_transparent = Button(415, 200, buy_img_transparent, 1)
buy_button_pikachu_transparent = Button(800, 200, buy_img_transparent, 1)


#zmiana napisy
max_speed_text_visible = True
max_speed_last_toggle_time = time.time()
max_speed_toggle_interval = 0.5
toggle_font_size = True


def load_gif_frames(gif_path, target_size):
    gif = Image.open(gif_path)
    frames = [] # Lista do przechowywania klatek

    try:
        while True:
            frame = gif.convert("RGBA") # Konwertuje bieżącą klatkę do formatu RGBA (przezroczystość)
            frame = pygame.image.fromstring(frame.tobytes(), frame.size, frame.mode) # Konwertuje klatkę na format Pygame (Surface)
            frames.append(frame.convert_alpha()) # Dodaje klatkę do listy frames
            gif.seek(gif.tell() + 1) # przechodzenie do nastepnej klatki
    except EOFError: #gdy gif.seek() isiagnie koniec pliku gif
        pass
    return frames

# Ładowanie klatek GIF-a
gif_path = 'dino_background_menu.gif'
gif_frames = load_gif_frames(gif_path, (width, height))
current_frame_index = 0
frame_duration = 0.1  # Czas trwania klatki w sekundach
last_frame_time = time.time()

def draw_text(text, font, color, x, y):
    img = font.render(text, True, WHITE)
    window.blit(img, (x, y))

def restart_game():
    global speed, score_music, courent_time, game_paused, menu_state, resume

    speed = 8
    score_music = 0
    courent_time = time.time()
    game_paused = False
    if resume:
        resume = False
        menu_state = "main"

    game_over.sound_played = False
    cash.sound_played_cash = False

    dino.x_cord = 30
    dino.y_cord = 190
    dino.ver_velocity = 0
    dino.hor_velocity = 0
    dino.jumping = False
    dino.bend = False

    background.x1 = 0
    background.x2 = background.bg_width
    background.clouds = []

    cactus.is_collided = False
    cactus.cactus = []

    length.score = 0
    length.text = ""

def load_game(run, keys, event):
    global speed, score_music, courent_time, game_paused, time_to_see_cactus, money
    global max_speed_text_visible, max_speed_last_toggle_time, max_speed_toggle_interval
    global toggle_font_size, hi_score_bool, naruto_menu

    # White background
    window.fill(WHITE)


    # Miganie napisu MAX SPEED
    if speed == 27:
        current_time = time.time()
        if current_time - max_speed_last_toggle_time >= max_speed_toggle_interval:
            max_speed_text_visible = not max_speed_text_visible
            max_speed_last_toggle_time = current_time
            toggle_font_size = not toggle_font_size


        if max_speed_text_visible:
            font = pygame.font.Font('Font/PressStart2P-Regular.ttf', 22)
            window.blit(font.render(f'M A X  S P E E D ! ! !', True, (255, 5, 18)), (270, 50))


    if length.score // 100 > score_music:
        score_music = length.score // 100
        length.every_hundred.play()
        if speed != 27:
            speed = speed * 1.05
        cactus.speed_spawn_cactus *= 2
        cactus.spawn_time1 /= 2
        cactus.spawn_time2 /= 2

    # Tick
    if not cactus.is_collided:
        dino.tick(keys)
        background.tick(speed)
        if (time.time() - courent_time) >= time_to_see_cactus:
            cactus.tick(speed, width, dino)
            if length.score > 60:
                cash.tick(speed, width, dino, cactus.cactus)
        length.tick(speed)

    # Draw
    background.draw(window)
    dino.draw(window, cactus.is_collided, naruto_menu)
    if (time.time() - courent_time) > time_to_see_cactus:
        cactus.draw(window, pika_menu)
        if length.score > 60:
            cash.draw(window, cactus.is_collided)
    length.draw(window, hi_score_bool)


    # Kolizja
    if cactus.is_collided:  # Sprawdzenie, czy doszło do kolizji
        game_over.tick(length.score)
        game_over.draw(window)
        speed = 0
        hi_score_bool = True
        if restart_button2.draw(window):
            restart_game()

    if cash.is_collided_cash:
        money += 1
        cash.is_collided_cash = False

    # Update
    pygame.display.update()

def main():
    global speed, score_music, courent_time, game_paused, menu_state
    global dino_menu, naruto_menu, pika_menu, money, pika_locked, naruto_locked
    global current_frame_index, last_frame_time
    run = True
    clock = 0

    font = pygame.font.Font('Font/PressStart2P-Regular.ttf', 30)
    font_buy = pygame.font.Font('Font/PressStart2P-Regular.ttf', 20)
    buy_skins_mp3 = pygame.mixer.Sound(f'mp3/buy_skin.mp3')


    while run:
        clock += pygame.time.Clock().tick(60) / 1000  # max 60 fps
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_paused = not game_paused

        keys = pygame.key.get_pressed()
        x_tex_money, y_tex_money = 370, 20
        x_uken, y_uken = 130, 230
        color_text = (36, 37, 38)
        #window.fill((200, 200, 200))

        # Display GIF frames
        window.blit(gif_frames[current_frame_index], (0, 0))


        if menu_state == "main":

            window.blit(font.render(f'MONEY: {money}$', True, color_text), (x_tex_money, y_tex_money))
            window.blit(font.render(f'--- D I N O  U K E N ---', True, color_text), (x_uken, y_uken))
            if start_button.draw(window):
               menu_state = "play"
            elif change_button.draw(window):
                menu_state = "characters"
                time.sleep(0.5)
            elif quit_button.draw(window):
                run = False

        elif menu_state == "characters":
            window.blit(font.render(f'MONEY: {money}$', True, color_text), (x_tex_money, y_tex_money))
            window.blit(font.render(f'--- D I N O  U K E N ---', True, color_text), (x_uken, y_uken))

            if naruto_locked:
                window.blit(font_buy.render(f'100$', True, color_text), (455, 75))

            if pika_locked:
                window.blit(font_buy.render(f'200$', True, color_text), (835, 75))


            if dino_button.draw(window):
                dino_menu = True
                naruto_menu = False
                pika_menu = False
                background.update_background(dino_menu, naruto_menu, pika_menu)
                dino.update_character(dino_menu, naruto_menu, pika_menu)  # Update character
                cactus.update_cactus( dino_menu, naruto_menu, pika_menu)
                time.sleep(0.5)
                menu_state = "play"

            if not naruto_locked:
                if naruto_button.draw(window):
                    dino_menu = False
                    naruto_menu = True
                    pika_menu = False
                    background.update_background(dino_menu, naruto_menu, pika_menu)
                    dino.update_character(dino_menu, naruto_menu, pika_menu)  # Update character
                    cactus.update_cactus(dino_menu, naruto_menu, pika_menu)
                    time.sleep(0.5)
                    menu_state = "play"

            elif naruto_locked:
                if naruto_button_locked.draw(window):
                    pass

                if money < 100:
                    if buy_button_naruto_transparent.draw(window):
                        pass
                elif money >= 100:
                    if buy_button_naruto.draw(window):
                        money = money - 100
                        buy_skins_mp3.play()
                        naruto_locked = False




            if not pika_locked:
                if pikachu_button.draw(window):
                    dino_menu = False
                    naruto_menu = False
                    pika_menu = True
                    background.update_background(dino_menu, naruto_menu, pika_menu)
                    dino.update_character(dino_menu, naruto_menu, pika_menu)  # Update character
                    cactus.update_cactus(dino_menu, naruto_menu, pika_menu)
                    time.sleep(0.5)
                    menu_state = "play"

            elif pika_locked:
                if pikachu_button_locked.draw(window):
                    pass
                if money < 200:
                    if buy_button_pikachu_transparent.draw(window):
                        pass
                elif money >= 200:
                    if buy_button_pikachu.draw(window):
                        money = money - 200
                        buy_skins_mp3.play()
                        pika_locked = False

        elif menu_state == "play":
            if game_paused:
                #window.fill((200, 200, 200))
                window.blit(font.render(f'MONEY: {money}$', True, color_text), (x_tex_money, y_tex_money))
                window.blit(font.render(f'--- D I N O  U K E N ---', True, color_text), (x_uken, y_uken))
                resume = True
                if resume_button.draw(window):
                    time.sleep(0.1)
                    game_paused = not game_paused
                    load_game(run, keys, event)
                if restart_button.draw(window):
                    restart_game()
                    time.sleep(0.5)
                    menu_state = "main"
                if quit_button.draw(window):
                    run = False
            else:
                load_game(run, keys, event)

        # Wyświetlanie GIF-a na całym ekranie
        current_time = time.time()
        if current_time - last_frame_time > frame_duration:
            current_frame_index = (current_frame_index + 1) % len(gif_frames)
            last_frame_time = current_time

        pygame.display.update()

if __name__ == '__main__':
    main()
