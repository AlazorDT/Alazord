from random import randint
from pygame import *

from time import time as timer

'''окно'''
win_width = 700
win_height = 500
display.set_caption('StarWars')
win = display.set_mode((win_width, win_height))
background = transform.scale(image.load('galaxy.jpg'), (win_width, win_height))

'''фон музыка'''
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')

'''пишем текст на экране'''
font.init()
font1 = font.SysFont(None, 80)
winner = font1.render('ПОБЕДА', True, (0, 255, 0))
lose = font1.render('ПОРАЖЕНИЕ', True, (188, 0, 0))
font2 = font.SysFont(None, 36)

goal = 30
score = 0
lost = 0
max_lost = 3
life = 3

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)
        '''спрайты хранят картинку'''
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        '''спрайты - прямоугольники "rectangle" '''
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        '''отрисовка героя на окне'''
        win.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    '''класс игрока'''
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_a] and self.rect.x > 10:
            self.rect.x -= self.speed

        if keys_pressed[K_d] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
    def fire(self):
        '''стрельба'''
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)

class Enemy(GameSprite):
    '''класс спрайта врага'''
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost += 1

class Bullet(GameSprite):
    '''класс спрайта пули'''
    def update(self):
        '''движение пули'''
        self.rect.y += self.speed
        '''исчезает, доходя до края экрана'''
        if self.rect.y < 0:
            self.kill()

class Asteroids(GameSprite):
    '''класс астероида'''
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > win_height:
            self.rect.x = randint(30, win_width - 30)
            self.rect.y = 0

'''создаем спрайты'''
ship = Player('rocket.png', 5, win_height - 100, 80, 100, 10)

monsters = sprite.Group()
for i in range(1, 6):
    monster = Enemy('ufo.png', randint(80, win_width - 80), -43, 80, 50, randint(1, 5))
    monsters.add(monster)

asteroids = sprite.Group()
for i in range(1, 3):
    asteroid = Asteroids('asteroid.png', randint(30, win_width - 30), -40, 80, 50, randint(1, 7))
    asteroids.add(asteroid)

bullets = sprite.Group()

'''игра закончилась'''
finish = False
'''осн цикл игры'''
run = True

num_fire = 0
rel_time = False

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                '''сколько выстрелов сделано'''
                if num_fire < 5 and rel_time == False:
                    num_fire += 1
                    fire_sound.play()
                    ship.fire()
                if num_fire >= 5 and rel_time == False:
                    last_time = timer()
                    rel_time = True

    if not finish:
        win.blit(background, (0, 0 ))

        '''пишет тект на экране'''
        text = font2.render('Счет:' + str(score), 1, (255, 255, 255))
        win.blit(text, (10, 20))

        text_lose = font2.render('Пропущено:' + str(lost), 1, (255, 255, 255))
        win.blit(text_lose, (10, 50))

        '''движ спрайтов'''
        monsters.update()
        ship.update()
        bullets.update()
        asteroids.update()
        '''обновляем местоположение спрайтов'''
        ship.reset()
        monsters.draw(win)
        bullets.draw(win)
        asteroids.draw(win)

        '''перезарядка'''
        if rel_time == True:
            now_time = timer()
            if now_time - last_time < 3:
                reload = font2.render('Wait! Reloading...', 1, (150, 0, 0))
                win.blit(reload, (260, 460))
            else:
                num_fire = 0
                rel_time = False

        '''проверка столкновения пули и монстров'''
        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score += 1
            monster = Enemy('ufo.png', randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)

        '''уменшение жизни, если спрайт коснулся врага'''
        if sprite.spritecollide(ship, monsters, False) or sprite.spritecollide(ship, asteroids, False):
            sprite.spritecollide(ship, monsters, True)
            sprite.spritecollide(ship, asteroids, True)
            life -= 1

        '''Поражение'''
        if life == 0 or lost >= max_lost:
            finish = True
            win.blit(lose, (170, 200))

        '''Победа'''
        if score >= goal:
            finish = True
            win.blit(winner, (170, 200))

        if life == 3:
            life_color = (0, 150, 0)
        if life == 2:
            life_color = (150, 150, 0)
        if life == 1:
            life_color = (150, 0, 0)

        text_life = font1.render(str(life), 1, life_color)
        win.blit(text_life, (650, 10))

        display.update()
    time.delay(60)

