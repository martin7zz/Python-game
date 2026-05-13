import os

import pygame

BASE_IMG_PATH = 'data/pictures/'


class Animation:
    def __init__(self, frames, fps=6, loop=True):
        self.frames = frames
        self.loop = loop
        self.fps = fps

        self.frame_index = 0
        self.time_acc = 0
        self.done = False

        self.frame_time = 120 / fps

    def copy(self):
        return Animation(self.frames, self.fps, self.loop)

    def update(self):
        if self.done:
            return

        self.time_acc += 1

        if self.time_acc >= self.frame_time:
            self.time_acc = 0
            self.frame_index += 1

            if self.frame_index >= len(self.frames):
                if self.loop:
                    self.frame_index = 0
                else:
                    self.frame_index = len(self.frames) - 1
                    self.done = True

    def img(self):
        return self.frames[self.frame_index]