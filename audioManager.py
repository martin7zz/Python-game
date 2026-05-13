import os, pygame
from sfxManager import SFXManager
from musicManager import MusicManager

class AudioManager:
    def __init__(self):
        self.music_manager = MusicManager()
        self.sfx_manager = SFXManager()
        self.master_volume = 1.0
        self.muted = False
        
    def set_master_volume(self, volume):
        self.music_manager.set_volume(volume)
        
        for sfx in self.sfx_manager.audio.values():
            sfx.set_volume(volume)