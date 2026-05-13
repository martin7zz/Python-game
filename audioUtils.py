import pygame
import os

BASE_SFX_PATH = 'data/sfx/'

class Audio:
    def __init__(self, path, volume=1.0):
        self.base_volume = volume
        self.sound = pygame.mixer.Sound(
            os.path.join(BASE_SFX_PATH, path)
        )
        self.sound.set_volume(volume)

    def play(self):
        self.sound.play()

    def stop(self):
        self.sound.stop()
    
    def set_volume(self, master_volume):
        self.sound.set_volume(
            self.base_volume * master_volume)