import pygame, os

BASE_MUSIC_PATH = 'data/music/'

class MusicManager:
    def __init__(self):
        self.current = None
        self.base_volume = 1.0

    def play(self, path, loop=-1, volume=1.0):
        full_path = os.path.join(BASE_MUSIC_PATH, path)
        
        self.base_volume = volume

        pygame.mixer.music.load(full_path)
        pygame.mixer.music.set_volume(self.base_volume)
        pygame.mixer.music.play(loop)

        self.current = path

    def stop(self):
        pygame.mixer.music.stop()

    def pause(self):
        pygame.mixer.music.pause()

    def unpause(self):
        pygame.mixer.music.unpause()
        
    def set_volume(self, master_volume):
        pygame.mixer.music.set_volume(self.base_volume * master_volume)


        