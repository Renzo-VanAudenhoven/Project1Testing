import pygame
import os


class SoundLibrary:
   
    def get_sound_lib(self):
        return self.find_audio_files
    
    def play(self, sound):
        pygame.mixer.Sound.play(self.get_sound_lib()[sound])
    
    def find_audio_files():
        rootdir = 'assets\sounds'
        sound_list = []
        for subdir, dirs, files in os.walk(rootdir):
            for file in files:
                sound_list.append(rootdir + "\\" + os.path.join(file))
        return sound_list

    def play_random_explosion(soundlib, noise):
        sound = pygame.mixer.Sound(soundlib[noise])
        if noise == 6:
            sound.set_volume(0.05)
        else:
            sound.set_volume(0.025)
        pygame.mixer.Sound.play(sound)