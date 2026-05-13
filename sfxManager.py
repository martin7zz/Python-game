import pygame, os
from audioUtils import Audio

class SFXManager:
    def __init__(self):
        self.audio = {}

    def load_all(self):
        for file in os.listdir('data/sfx/'):
            if file.endswith('.wav') or file.endswith('.mp3'):
                name = os.path.splitext(file)[0]
                self.audio[name] = Audio(file)

    def play(self, name):
        sound = self.get_audio(name)

        if sound:
            sound.play()
    
    def get_audio(self, name):
        sound = self.audio.get(name)
        
        return sound