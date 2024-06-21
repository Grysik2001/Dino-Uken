import pygame
from math import floor
from random import randint, uniform
import time

class Physic:
    def __init__(self, x, y, width, height, image):
        self.x_cord = x
        self.y_cord = y
        self.width = width
        self.height = height
        self.ver_velocity = 0
        self.hor_velocity = 0
        self.jumping = False
        self.gravity = 1.2

        self.image = image.convert_alpha()
        self.hitbox = pygame.mask.from_surface(self.image)

    def physic_tick(self):
        self.ver_velocity += self.gravity
        self.y_cord += self.ver_velocity
        self.hitbox = pygame.mask.from_surface(self.image)  # Update the mask based on current image
        self.hitbox_rect = self.image.get_rect(topleft=(self.x_cord, self.y_cord))

        if self.y_cord > 170:
            self.y_cord = 170
            self.jumping = False
            self.ver_velocity = 0

        self.x_cord += self.hor_velocity

class Dino(Physic):
    def __init__(self, x, y, dino_menu, naruto_menu, pika_menu):
        self.update_character(dino_menu, naruto_menu, pika_menu)
        #self.img_dino_bend = []
        self.img_start = pygame.image.load(f'png/Chrome_Dino/Dino/start.png') #?????
        self.mp3_jump = pygame.mixer.Sound(f'mp3/jump.mp3')
        self.walk_index = 1
        self.bend = False

        self.jumping = False
        self.jumping_start = False

        if self.bend and len(self.img_dino_bend) > 0:
            width = self.img_dino_bend[self.walk_index].get_width()
            height = self.img_dino_bend[self.walk_index].get_height()
        elif self.jumping:
            width = self.jump.get_width()
            height = self.jump.get_height()
        else:
            width = self.img_dino[self.walk_index].get_width()
            height = self.img_dino[self.walk_index].get_height()

        super().__init__(x, y, width, height, self.img_dino[0])

    def update_character(self, dino_menu, naruto_menu, pika_menu):
        if dino_menu:
            self.img_dino = [pygame.image.load(f'png/Chrome_Dino/Dino/walk/skin1_{x}.png') for x in range(1, 3)] #animacja chodzenia
            self.img_dino_bend = [pygame.image.load(f'png/Chrome_Dino/Dino/bend/skin1_{x}.png') for x in
                             range(7, 9)]  # animacja schylania sie
            self.img_jump = pygame.image.load(f'png/Chrome_Dino/Dino/jump.png')
            self.img_death= pygame.image.load(f'png/Chrome_Dino/Dino/game_over.png')

        elif naruto_menu:
            self.img_dino = [pygame.image.load(f'png/Naruto/walk/nar{x}.png')
                             for x in range(1, 5)]  # animacja chodzenia
            self.img_dino_bend = [pygame.image.load(f'png/Naruto/bend/nar_bend{x}.png')
                                  for x in range(1, 3)]  # animacja schylania sie
            self.img_jump = pygame.image.load(f'png/Naruto/nar_jump.png')
            self.img_death = pygame.image.load(f'png/Naruto/nar_death.png')

        elif pika_menu:
            self.img_dino = [pygame.image.load(f'png/Pikachu/walk/pika{x}.png') for x in
                             range(1, 3)]  # animacja chodzenia
            self.img_dino_bend = [pygame.image.load(f'png/Pikachu/bend/pika_bend{x}.png') for x in
                                  range(1, 3)]  # animacja schylania sie
            self.img_jump = pygame.image.load(f'png/Pikachu/jump/pika_jump1.png')
            self.img_death = pygame.image.load(f'png/Pikachu/pika_death.png')


    def tick(self, keys):
        #jumping
        self.physic_tick()

        if keys[pygame.K_SPACE] and self.jumping is False and self.bend is False:
            self.ver_velocity -= 20
            self.jumping = True
            self.mp3_jump.play()
        #schylanie sie
        if keys[pygame.K_DOWN]:
            self.bend = True
            self.gravity = 1.8
        else:
            self.bend = False
            self.gravity = 1.3

    def draw(self, window, is_collided, naruto_menu):
        if is_collided:
            window.blit(self.img_death, (self.x_cord, self.y_cord))
        elif self.jumping and self.bend and self.img_dino_bend:
            index = int(self.walk_index) % len(self.img_dino_bend)  # Użyj modulo, aby zapętlać animację
            window.blit(self.img_dino_bend[index], (self.x_cord, self.y_cord + 30))
        elif self.jumping:
            window.blit(self.img_jump, (self.x_cord, self.y_cord))
        elif self.bend and self.img_dino_bend:
            index = int(self.walk_index) % len(self.img_dino_bend)  # Użyj modulo, aby zapętlać animację
            if naruto_menu:
                window.blit(self.img_dino_bend[index], (self.x_cord, self.y_cord + 10))
            else: window.blit(self.img_dino_bend[index], (self.x_cord, self.y_cord + 30))
            self.walk_index += 0.25
        elif self.img_dino:
            index = int(self.walk_index) % len(self.img_dino)  # Użyj modulo, aby zapętlać animację
            window.blit(self.img_dino[index], (self.x_cord, self.y_cord))
            self.walk_index += 0.25

class GameOver():
    def __init__(self, x, y):
        self.x_cord = x
        self.y_cord = y
        self.font = pygame.font.Font('Font/PressStart2P-Regular.ttf', 16)
        self.text = self.font.render("G A M E  O V E R", True, (62, 64, 66))
        self.game_over_mp3 = pygame.mixer.Sound(f'mp3/game_over.mp3')
        self.sound_played = False


    def tick(self, score):
        if not self.sound_played:
            self.game_over_mp3.play()
            self.sound_played = True

    def draw(self, window):
        window.blit(self.text, (self.x_cord, self.y_cord))

class HowFar(GameOver):
    def __init__(self, x, y):
        self.x_cord = x
        self.y_cord = y
        self.font = pygame.font.Font('Font/PressStart2P-Regular.ttf', 16)
        self.score = 0
        self.text = ""
        self.hi_score = 0
        self.text_hi_score = self.font.render(f'HI {self.zero(self.score)}', True, (62, 64, 66))
        self.record = 0
        self.every_hundred = pygame.mixer.Sound(f'mp3/100pkt.mp3')

    def zero(self, number):
        number = round(number)
        if number < 10:
            return f"0000{number}"
        elif number < 100:
            return f"000{number}"
        elif number < 1000:
            return f"00{number}"
        elif number < 10000:
            return f"0{number}"
        elif number < 100000:
            return f"{number}"
        elif number == 100000:
            return f"omg error"

    def tick(self, speed):
        self.score += speed * 0.018 #f"{self.length}"
        self.text = self.font.render(f"{self.zero(self.score)}", True, (62, 64, 66))

        if self.score > self.hi_score:
           self.hi_score = self.score
           self.text_hi_score = self.font.render(f"HI {self.zero(self.hi_score)}", True, (62, 64, 66))

    def draw(self, window, hi_score_bool):
        window.blit(self.text, (self.x_cord, self.y_cord))

        if hi_score_bool:
            window.blit(self.text_hi_score, (self.x_cord - 150, self.y_cord))



class Cactus():
    def __init__(self, x, y, dino_menu, naruto_menu, pika_menu, speed):
        self.update_cactus(dino_menu, naruto_menu, pika_menu)

        self.x_cord = x
        self.y_cord = y
        self.cactus = []
        self.spawn_time_cactus = time.time() #czas rozpoczęcia
        self.is_collided = False

        self.speed_spawn_cactus = 8.3

        if 12 <= speed < 20:
            self.spawn_time1 = 0.067
            self.spawn_time2 = 0.095
        elif speed >= 20:
            self.spawn_time1 = 0.065
            self.spawn_time2 = 0.08
        elif speed == 27:
            self.spawn_time1 = 0.064
            self.spawn_time2 = 0.08
        elif speed < 12:
            self.spawn_time1 = 0.1
            self.spawn_time2 = 0.12


        #super().__init__(x, y, self.cactus["img"].get_width(), self.cactus["img"].get_height(), self.cactus["img"])

    def update_cactus(self, dino_menu, naruto_menu, pika_menu):
        if dino_menu:
            self.img_cactus = [pygame.image.load(f'png/Chrome_Dino/Cactus/kaktus1_{x}.png') for x in range(1, 13)] #lista scieżek wszyskich kakatusów
        elif naruto_menu:
            self.img_cactus = [pygame.image.load(f'png/Naruto/city/city{x}.png') for x in range(1, 8)] #lista scieżek wszyskich kakatusów
        elif pika_menu:
            self.img_cactus = [pygame.image.load(f'png/Pikachu/forest/forest{x}.png') for x in range(1, 8)] #lista scieżek wszyskich kakatusów


    def spawn_cactus(self, speed):
        new_cactus = { #do każdego kaktusa przydzielam img oraz współrzedną x
            "img": self.img_cactus[randint(0, len(self.img_cactus) - 1)],
            "x" : self.x_cord,
        }
        self.cactus.append(new_cactus)
        self.spawn_time_cactus = time.time() + uniform(self.spawn_time1 * self.speed_spawn_cactus, self.spawn_time2 * self.speed_spawn_cactus) #czas po którym pojawi się następny kaktus


    def tick(self, speed, width, dino):
        current_time_cactus = time.time()
        if current_time_cactus >= self.spawn_time_cactus:
            self.spawn_cactus(speed)

        for cactus in self.cactus:
            cactus["x"] -= speed
            cactus_mask = pygame.mask.from_surface(cactus["img"])
            offset = (cactus["x"] - dino.x_cord, self.y_cord - dino.y_cord)
            if dino.hitbox.overlap(cactus_mask, offset):
                self.is_collided = True

        #usuwanie z ekranu kaktusów
        self.cactus = [cactus for cactus in self.cactus if cactus["x"] > - cactus["img"].get_width()]


    def draw(self, window, pika_menu):
        if not pika_menu:
            for cactus in self.cactus:
                window.blit(cactus["img"], (cactus["x"], self.y_cord))
        elif pika_menu:
            for cactus in self.cactus:
                window.blit(cactus["img"], (cactus["x"], self.y_cord + 10))
class Background:
    def __init__(self, x, y, dino_menu, naruto_menu, pika_menu):
        self.update_background(dino_menu, naruto_menu, pika_menu)

        self.bg_width = self.img_bg.get_width()
        self.x1 = 0
        self.x2 = self.bg_width

        self.spawn_time_cloud = time.time()  # czas rozpoczęcia
        self.cloud_width = self.img_cloud.get_width()
        self.clouds = []
        self.clouds_x, self.clouds_y = 10, 120

        self.y = y
        self.x = x


    def update_background(self, dino_menu, naruto_menu, pika_menu):
        if dino_menu:
            self.img_bg = pygame.image.load('png/Chrome_Dino/Background/background.png')
            self.img_cloud = pygame.image.load('png/Chrome_Dino/Background/cloud.png')
        elif naruto_menu:
            self.img_bg = pygame.image.load('png/Naruto/background/nar_background.png')
            self.img_cloud = pygame.image.load('png/Naruto/background/nar_clouds.png')
        elif pika_menu:
            self.img_bg = pygame.image.load('png/Pikachu/background/pika_background.png')
            self.img_cloud = pygame.image.load('png/Pikachu/background/pika_clouds.png')


    def spawn_cloud(self, speed):
        new_cloud = {
            "x": self.x,
            "y" : randint(self.clouds_x, self.clouds_y)
        }
        self.clouds.append(new_cloud)
        self.spawn_time_cloud = time.time() + uniform(speed*0.7, speed*0.9)  # czas po którym pojawi się następny kaktus

    def tick(self, speed):
        #no end background
        self.x1 -= speed
        self.x2 -= speed
        if self.x1 <= -self.bg_width:
            self.x1 = self.bg_width
        if self.x2 <= -self.bg_width:
            self.x2 = self.bg_width

        #no end cloud
        current_time = time.time()
        if current_time >= self.spawn_time_cloud:
            self.spawn_cloud(speed)

        for cloud in self.clouds:
            cloud["x"] -= speed * 0.15

        #usunięcie chmur z ekranu
        self.clouds = [cloud for cloud in self.clouds if cloud["x"] > -self.cloud_width] #chmura poza lewą krawedzia usuwana jest z listy

    def draw(self, window):
        window.blit(self.img_bg, (self.x1, self.y))
        window.blit(self.img_bg, (self.x2, self.y))


        for cloud in self.clouds:
            window.blit(self.img_cloud, (cloud["x"], cloud["y"]))


class Button():
	def __init__(self, x, y, image, scale):
		width = image.get_width()
		height = image.get_height()
		self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
		self.rect = self.image.get_rect()
		self.rect.topleft = (x, y)
		self.clicked = False

	def draw(self, surface):
		action = False
		#get mouse position
		pos = pygame.mouse.get_pos()

		#check mouseover and clicked conditions
		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				self.clicked = True
				action = True

		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False

		#draw button on screen
		surface.blit(self.image, (self.rect.x, self.rect.y))

		return action

class Cash:
    def __init__(self, x, y):
        self.x_cord = x
        self.cash = []
        self.spawn_time_cash = time.time()
        self.is_collided_cash = False
        self.speed_spawn_cash = 10
        self.spawn_time1 = 0.1
        self.spawn_time2 = 1
        self.index_cash = 0
        self.img_cash = [pygame.image.load(f'coin/money{x}.png') for x in range(1, 11)]
        self.sound_played_cash = False
        self.cash_mp3 = pygame.mixer.Sound(f'mp3/coin.mp3')


    def spawn_cash(self, speed, cactus_list):
        new_cash = {
            "y": randint(20, 200),
            "x": self.x_cord
        }
        #warunek sprawdzajacy czy cash nie pojawi sie na kaktusie
        while any(abs(new_cash["x"] - cactus["x"]) < 60 for cactus in cactus_list):
            new_cash["x"] = randint(60, 960)

        self.cash.append(new_cash)
        self.spawn_time_cash = time.time() + uniform(self.spawn_time1 * self.speed_spawn_cash, self.spawn_time2 * self.speed_spawn_cash)

    def tick(self, speed, width, dino, cactus_list):
        current_time_cash = time.time()
        if current_time_cash >= self.spawn_time_cash:
            self.spawn_cash(speed, cactus_list)

        for cash in self.cash:
            cash["x"] -= speed
            cash_mask = pygame.mask.from_surface(self.img_cash[floor(self.index_cash)])
            offset = (cash["x"] - dino.x_cord, cash["y"] - dino.y_cord)
            if dino.hitbox.overlap(cash_mask, offset):
                self.is_collided_cash = True
                self.cash_mp3.play()
                if not self.sound_played_cash:
                    self.sound_played_cash = True
                self.cash.remove(cash)  # usuwanie elemntu z listy

        self.cash = [cash for cash in self.cash if cash["x"] > - self.img_cash[floor(self.index_cash)].get_width()]

    def draw(self, window, is_collided_cactus):
        if is_collided_cactus:
            pass
        else:
            for cash in self.cash:
                window.blit(self.img_cash[floor(self.index_cash)], (cash["x"], cash["y"]))
                self.index_cash += 0.25
                if self.index_cash >= len(self.img_cash):
                    self.index_cash = 0
