import os
import pygame
from PIL import Image
from pygame import mixer
import random
import numpy as np
import IKPHBV.Buddy.game.detect_mask_video as dmv

pygame.mixer.pre_init(44100, -16, 2, 512)
mixer.init()
pygame.init()

music = 'music/game.mp3'

icon = pygame.image.load("img/mini_corona.png")
pygame.display.set_icon(icon)

mouse = pygame.mouse.get_pos()

pygame.mixer.music.load(music)
pygame.mixer.music.set_volume(0.3)
# pygame.mixer.music.play()

# define fps
clock = pygame.time.Clock()
fps = 60

screen_width = 600
screen_height = 800

# buttons
button_x = 650
button_color = (255, 255, 255)
button_light = (170, 170, 170)
button_dark = (100, 100, 100)
button_font = pygame.font.SysFont('Corbel', 35)
quit_text = button_font.render('QUIT', True, button_color)
retry_text = button_font.render('RETRY', True, button_color)

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('CoFight-19')

# define fonts
font30 = pygame.font.SysFont('Constantia', 30)
font40 = pygame.font.SysFont('Constantia', 40)
fontGame = pygame.font.SysFont('Bebas', 50)

# load sounds
explosion_fx = pygame.mixer.Sound("music/explosion.wav")
explosion_fx.set_volume(0.15)

explosion2_fx = pygame.mixer.Sound("music/explosion2.wav")
explosion2_fx.set_volume(0.15)

laser_fx = pygame.mixer.Sound("music/laser.wav")
laser_fx.set_volume(0.15)

# define game variables
rows = 5
cols = 5
alien_cooldown = 1000  # bullet cooldown in milliseconds
last_alien_shot = pygame.time.get_ticks()
countdown = 5
last_count = pygame.time.get_ticks()
game_over = 0  # 0 is no game over, 1 means player has won, -1 means player has lost

# define colours
red = (255, 0, 0)
green = (0, 255, 0)
white = (255, 255, 255)

# load image
bg = pygame.image.load("img/background.png")


def draw_bg():
    screen.blit(bg, (0, 0))


# define function for creating text
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


# create spaceship class
class Spaceship(pygame.sprite.Sprite):
    def __init__(self, x, y, health):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("img/roi.png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.heart = pygame.image.load("img/heart.png")
        self.heart_rect = self.heart.get_rect()
        self.heart_y = 30
        self.health_start = health
        self.health_remaining = health
        self.last_shot = pygame.time.get_ticks()

    def update(self):
        # set movement speed
        speed = 8
        # set a cooldown variable
        cooldown = 500  # milliseconds
        game_over = 0

        # get key press
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= speed
        if key[pygame.K_RIGHT] and self.rect.right < screen_width:
            self.rect.x += speed

        # record current time
        time_now = pygame.time.get_ticks()
        # shoot
        if key[pygame.K_SPACE] and time_now - self.last_shot > cooldown:
            laser_fx.play()
            bullet = Bullets(self.rect.centerx, self.rect.top)
            bullet_group.add(bullet)
            self.last_shot = time_now

        # update mask
        self.mask = pygame.mask.from_surface(self.image)

        # draw health bar
        # pygame.draw.rect(screen, red, (self.rect.x, (self.rect.bottom + 10), self.rect.width, 15))
        if self.health_remaining == 3:
            screen.blit(self.heart, ((self.rect.x - 25), (self.rect.bottom + 10)))
            screen.blit(self.heart, ((self.rect.x + 5), (self.rect.bottom + 10)))
            screen.blit(self.heart, ((self.rect.x + 35), (self.rect.bottom + 10)))

        elif self.health_remaining == 2:
            screen.blit(self.heart, ((self.rect.x - 25), (self.rect.bottom + 10)))
            screen.blit(self.heart, ((self.rect.x + 5), (self.rect.bottom + 10)))

        elif self.health_remaining == 1:
            screen.blit(self.heart, ((self.rect.x - 25), (self.rect.bottom + 10)))

            # pygame.draw.rect(screen, green, (
            # self.rect.x, (self.rect.bottom + 10), int(self.rect.width * (self.health_remaining / self.health_start)),
            # 15))
        elif self.health_remaining <= 0:
            explosion = Explosion(self.rect.centerx, self.rect.centery, 3)
            explosion_group.add(explosion)
            self.kill()
            game_over = -1
        return game_over


# create Bullets class
class Bullets(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("img/vaccine.png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

    def update(self):
        self.rect.y -= 5
        if self.rect.bottom < 0:
            self.kill()
        if pygame.sprite.spritecollide(self, alien_group, True):
            self.kill()
            explosion_fx.play()
            explosion = Explosion(self.rect.centerx, self.rect.centery, 2)
            explosion_group.add(explosion)


# create Aliens class
class Aliens(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("img/wappie" + str(random.randint(1, 5)) + ".png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.move_counter = 0
        self.move_direction = 1

    def update(self):
        if wearingMask:
            self.rect.x += self.move_direction
            self.move_counter += 1

            if abs(self.move_counter) > 75:
                self.move_direction *= -1
                self.move_counter *= self.move_direction

        else:
            self.rect.x += self.move_direction
            self.rect.y += self.move_direction
            self.move_counter += 10

            if abs(self.move_counter) > 75:
                self.move_direction *= -1
                self.move_counter *= self.move_direction


# create Alien Bullets class
class Alien_Bullets(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("img/mini_corona.png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

    def update(self):

        if wearingMask:
            self.rect.y += 3
        else:
            self.rect.y += 100

        if self.rect.top > screen_height:
            self.kill()
        if pygame.sprite.spritecollide(self, spaceship_group, False, pygame.sprite.collide_mask):
            self.kill()
            explosion2_fx.play()
            # reduce spaceship health
            spaceship.health_remaining -= 1
            explosion = Explosion(self.rect.centerx, self.rect.centery, 1)
            explosion_group.add(explosion)


# create Explosion class
class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y, size):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        for num in range(1, 6):
            img = pygame.image.load(f"img/exp{num}.png")
            if size == 1:
                img = pygame.transform.scale(img, (20, 20))
            if size == 2:
                img = pygame.transform.scale(img, (40, 40))
            if size == 3:
                img = pygame.transform.scale(img, (160, 160))
            # add the image to the list
            self.images.append(img)
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.counter = 0

    def update(self):
        explosion_speed = 3
        # update explosion animation
        self.counter += 1

        if self.counter >= explosion_speed and self.index < len(self.images) - 1:
            self.counter = 0
            self.index += 1
            self.image = self.images[self.index]

        # if the animation is complete, delete explosion
        if self.index >= len(self.images) - 1 and self.counter >= explosion_speed:
            self.kill()


# create sprite groups
spaceship_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
alien_group = pygame.sprite.Group()
alien_bullet_group = pygame.sprite.Group()
explosion_group = pygame.sprite.Group()


def create_aliens():
    # generate aliens
    for row in range(rows):
        for item in range(cols):
            alien = Aliens(100 + item * 100, 100 + row * 70)
            alien_group.add(alien)


create_aliens()

def drawControls():
    draw_text('Use your arrow keys to move', font40, white, screen_width / 2 - 250, screen_height / 2 + 90)
    draw_text('Use Spacebar to fire!', font40, white, screen_width / 2 - 180, screen_height / 2 + 130)
    draw_text(str(countdown), font40, white, screen_width / 2 - 12, screen_height - 125)

# create player
spaceship = Spaceship(int(screen_width / 2), screen_height - 100, 3)
spaceship_group.add(spaceship)

# detect mask video results
result = dmv.startCam()
wearingMask = result[0]
heart_color = result[1]
photoTaken = result[2]

# make heart colour of mask video output
im = Image.open('img/heart.png')
data = np.array(im)
r1, g1, b1 = 255, 255, 255  # Original value
r2, g2, b2 = heart_color
red, green, blue = data[:, :, 0], data[:, :, 1], data[:, :, 2]
mask = (red == r1) & (green == g1) & (blue == b1)
data[:, :, :3][mask] = [r2, g2, b2]
im = Image.fromarray(data)
im.save('img/heart_fixed.png')

# set new images
spaceship.heart = pygame.image.load("img/heart_fixed.png")
spaceship.image = pygame.image.load("img/roi.png")

# more enemies if not wearing mask
if not wearingMask:
    alien_cooldown = -1  # bullet cooldown in milliseconds
    cols = 6

while photoTaken:

    clock.tick(fps)

    # draw background
    draw_bg()

    # draw sprite groups
    spaceship_group.draw(screen)
    bullet_group.draw(screen)
    alien_group.draw(screen)
    alien_bullet_group.draw(screen)
    explosion_group.draw(screen)

    if countdown == 0:
        # create random alien bullets
        # record current time
        time_now = pygame.time.get_ticks()
        # shoot
        if time_now - last_alien_shot > alien_cooldown and len(alien_bullet_group) < 5 and len(alien_group) > 0:
            attacking_alien = random.choice(alien_group.sprites())
            alien_bullet = Alien_Bullets(attacking_alien.rect.centerx, attacking_alien.rect.bottom)
            alien_bullet_group.add(alien_bullet)
            last_alien_shot = time_now

        # check if all the aliens have been killed
        if len(alien_group) == 0:
            game_over = 1

        if game_over == 0:
            # update spaceship
            game_over = spaceship.update()

            # update sprite groups
            bullet_group.update()
            alien_group.update()
            alien_bullet_group.update()

        else:

            # game over / you win when wearing mask text
            if wearingMask:
                if game_over == -1:
                    pygame.draw.rect(screen, (0, 0, 0), [int(screen_width / 2 - 110), int(screen_height / 2 + 47), 260, 40])
                    draw_text('GAME OVER!', font40, white, int(screen_width / 2 - 100), int(screen_height / 2 + 50))
                if game_over == 1:
                    pygame.draw.rect(screen, (0, 0, 0), [int(screen_width / 2 - 110), int(screen_height / 2 + 47), 215, 40])
                    draw_text('YOU WIN!', font40, white, int(screen_width / 2 - 100), int(screen_height / 2 + 50))

            # game over / you win when NOT wearing mask text
            else:
                if game_over == -1:
                    pygame.draw.rect(screen, (0, 0, 0), [int(screen_width / 2 - 107), int(screen_height / 2 + 68), 280, 40])
                    draw_text('u have the rona', font40, white, int(screen_width / 2 - 100),
                              int(screen_height / 2 + 70))
                if game_over == 1:
                    # wij hebben hier echt teveel moeite voor gedaan
                    draw_text('maat hoe dan, doe even niet, daar h', font40, white, 0, int(screen_height / 2 + 0))
                    draw_text('eb je sterke genen ofzo, vind dit ech', font40, white, 0, int(screen_height / 2 + 35))
                    draw_text('t niet kunnen, wij hebben zo ons b', font40, white, 0, int(screen_height / 2 + 65))
                    draw_text('est gedaan dit zo moeilijk mogelijk ', font40, white, 0, int(screen_height / 2 + 95))
                    draw_text('te maken, weet jij het een beetje te', font40, white, 0, int(screen_height / 2 + 125))
                    draw_text('beaten, echt heel jammer dit.', font40, white, 0, int(screen_height / 2 + 155))

            # hover over quit button
            if screen_width - 200 <= mouse[0] <= screen_width - 60 and button_x <= mouse[1] <= button_x + 40:
                pygame.draw.rect(screen, button_light, [screen_width - 200, button_x, 140, 40])
                pygame.draw.rect(screen, button_dark, [screen_width / 2 - 240, button_x, 140, 40])

            # hover over retry button
            elif screen_width / 2 - 240 <= mouse[0] <= screen_width / 2 - 100 and button_x <= mouse[1] <= button_x + 40:
                pygame.draw.rect(screen, button_dark, [screen_width - 200, button_x, 140, 40])
                pygame.draw.rect(screen, button_light, [screen_width / 2 - 240, button_x, 140, 40])

            # default buttons
            else:
                pygame.draw.rect(screen, button_dark, [screen_width - 200, button_x, 140, 40])
                pygame.draw.rect(screen, button_dark, [screen_width / 2 - 240, button_x, 140, 40])

            # text for buttons
            screen.blit(quit_text, (int(screen_width - 200 + 35), button_x + 5))
            screen.blit(retry_text, (int(screen_width / 2 - 240 + 23), button_x + 5))

    if countdown > 0:
        pygame.draw.rect(screen, (0, 0, 0), [int(screen_width / 2 - 260), int(screen_height / 2 + 85), 520, 90])
        drawControls()
        count_timer = pygame.time.get_ticks()
        if count_timer - last_count > 1000:
            countdown -= 1
            last_count = count_timer

    # update explosion group
    explosion_group.update()

    mouse = pygame.mouse.get_pos()

    # event handlers
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.display.quit()
            pygame.quit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            # mouse event for quit
            if screen_width - 200 <= mouse[0] <= screen_width - 60 and button_x <= mouse[1] <= button_x + 40:
                pygame.display.quit()
                pygame.quit()
            # mouse event for retry
            if screen_width / 2 - 240 <= mouse[0] <= screen_width / 2 - 100 and button_x <= mouse[1] <= button_x + 40:
                pygame.display.quit()
                pygame.quit()
                os.system("cofight.py")

    pygame.display.update()


