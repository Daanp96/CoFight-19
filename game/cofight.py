import os
import pygame
import pygame_menu
from pygame_menu.themes import Theme

pygame.init()
pygame.mixer.init()

pygame.display.set_caption('CoFight-19')

icon = pygame.image.load("img/mini_corona.png")
pygame.display.set_icon(icon)

music = 'music/title.mp3'

pygame.mixer.music.load(music)
pygame.mixer.music.play()


def start_the_game():
    pygame.display.quit()
    pygame.quit()
    os.system("game.py")
    print("[INFO] starting character selection...")

    pass


surface = pygame.display.set_mode((600, 400))

w, h = pygame.display.get_surface().get_size()

# font = pygame_menu.font.FONT_MUNRO
font = pygame_menu.font.FONT_BEBAS

ronaBackground = pygame_menu.baseimage.BaseImage(
    image_path="img/rona.jpg",
    drawing_mode=pygame_menu.baseimage.IMAGE_MODE_REPEAT_XY
)

cofightTheme = Theme(
    title_shadow=False,
    title_bar_style=pygame_menu.widgets.MENUBAR_STYLE_NONE,
    title_offset = (200, 50),
    widget_font=font,
    title_font= font,
    background_color = ronaBackground
)

menu = pygame_menu.Menu(400, 600, 'CoFight-19',
                        theme=cofightTheme)

menu.add_button('Play', start_the_game)
menu.add_button('Quit', pygame_menu.events.EXIT)

menu.mainloop(surface)
