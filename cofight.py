import pygame
import pygame_menu

pygame.init()
pygame.mixer.init()

pygame.display.set_caption('CoFight-19')

def start_the_game():
    # Do the job here !
    print("LETS GET IT")
    pass

aphex = 'bleh.mp3'

pygame.mixer.music.load(aphex)
pygame.mixer.music.play()

surface = pygame.display.set_mode((600, 400))

menu = pygame_menu.Menu(400, 600, 'CoFight-19',
                       theme=pygame_menu.themes.THEME_SOLARIZED)

menu.add_button('Play', start_the_game)
menu.add_button('Quit', pygame_menu.events.EXIT)

menu.mainloop(surface)