import sys 
import pygame
import pygame_menu

pygame.init()
pygame.mixer.init()

def set_difficulty():
    # Do the job here !
    pass

def start_the_game():
    # Do the job here !
    pass

# aphex = 'bleh.mp3'
#
# size = width, height = 320, 240
# speed = [2, 2]
# black = 128, 0, 128
#
# screen = pygame.display.set_mode(size)
#
# pygame.mixer.music.load(aphex)
# pygame.mixer.music.play()

surface = pygame.display.set_mode((600, 400))

menu = pygame_menu.Menu(240, 320, 'Welcome',
                       theme=pygame_menu.themes.THEME_BLUE)

menu.add_text_input('Name :', default='John Doe')
menu.add_selector('Difficulty :', [('Hard', 1), ('Easy', 2)], onchange=set_difficulty)
menu.add_button('Play', start_the_game)
menu.add_button('Quit', pygame_menu.events.EXIT)

menu.mainloop(surface)