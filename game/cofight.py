import pygame
import pygame_menu
import os

pygame.init()
pygame.mixer.init()

pygame.display.set_caption('CoFight-19')

music = 'music/bleh.mp3'

pygame.mixer.music.load(music)
pygame.mixer.music.play()

def start_the_game():
    os.system("game.py");
    print("LETS GET IT")
    pass

surface = pygame.display.set_mode((600, 400))

menu = pygame_menu.Menu(400, 600, 'CoFight-19',
                       theme=pygame_menu.themes.THEME_SOLARIZED)

menu.add_button('Play', start_the_game)
menu.add_button('Quit', pygame_menu.events.EXIT)

menu.mainloop(surface)
