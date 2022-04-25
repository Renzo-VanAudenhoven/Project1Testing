import pygame
#music player
def music_player():
    pygame.mixer.init()
    pygame.mixer.music.load("assets/music/good_music.ogg")
    pygame.mixer.music.set_volume(0.1)
    pygame.mixer.music.play(-1,17)