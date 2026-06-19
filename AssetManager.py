import pygame
from spriteSheet import SpriteSheet
from spriteUtils import Animation

BASE_IMG_PATH = 'data/pictures/'

class AssetManager:
    def __init__(self):
        self.assets = {}

    def load_all(self):
        self.load_player_assets()
        self.load_enemy_assets()

    def load_player_assets(self):
        self.assets['player/idle'] = Animation(
            SpriteSheet(
                BASE_IMG_PATH + 'Player/Sprites/IDLE.png'
            ).load_grid_images(
                num_rows=1,
                num_cols=10,
                x_margin=0,
                x_padding=0,
                y_margin=15,
                y_padding=15
            ),
            fps=10,
            loop=True
        )
        self.assets['player/run'] = Animation(
            SpriteSheet(
                BASE_IMG_PATH + 'Player/Sprites/RUN.png'
            ).load_grid_images(
                num_rows=1,
                num_cols=16,
                x_margin=0,
                x_padding=0,
                y_margin=15,
                y_padding=15
            ),
            fps=16,
            loop=True
        )
        self.assets['player/attack'] = Animation(
            SpriteSheet(BASE_IMG_PATH + 'Player/Sprites/ATTACK 1.png').load_grid_images(
                num_rows=1,
                num_cols=7,
                x_margin=0,
                x_padding=0,
                y_margin=15,
                y_padding=15
            ),
            fps=30,
            loop=False
        )

    def load_enemy_assets(self):
        self.assets['enemy/idle'] = Animation(
            SpriteSheet(BASE_IMG_PATH + 'Enemies/Mushroom/Mushroom without VFX/Mushroom-Idle.png').slice(1, 7),
            fps=15, loop=True
        )
        self.assets['enemy/run'] = Animation(
            SpriteSheet(BASE_IMG_PATH + 'Enemies/Mushroom/Mushroom without VFX/Mushroom-Run.png').slice(1, 8),
            fps=15, loop=True
        )
        self.assets['enemy/attack'] = Animation(
            SpriteSheet(BASE_IMG_PATH + 'Enemies/Mushroom/Mushroom without VFX/Mushroom-Attack.png').slice(1, 10),
            fps=20, loop=False
        )

    def get(self, key):
        return self.assets[key].copy()