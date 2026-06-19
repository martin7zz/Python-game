import pygame

PLAYER_ATTACKS = {
    "sword": {
        "light": {
            "anim": "attack",
            "duration": 30 / 60,        # ~0.833s
            "hitbox_start": 0 / 60,     # 0.0s
            "hitbox_end": 10 / 60,      # ~0.167s
            "hitbox": pygame.Rect(0, 0, 70, 30),
            "offsets": {
                "offset_x": 20,
                "offset_y": 20
            },
            "damage": {1: 30, 2: 45, 3: 60}, 
        },
        "heavy": {
            "anim": "attack_heavy",
            "duration": 70 / 60,        # ~1.167s
            "hitbox_start": 20 / 60,    # ~0.333s
            "hitbox_end": 40 / 60,      # ~0.667s
            "hitbox": pygame.Rect(0, 0, 90, 40),
            "offsets": {
                "offset_x": 20,
                "offset_y": 20
            },
            "damage": {1: 30, 2: 45, 3: 60}, 
        }
    }
}

ENEMY_ATTACKS = {
    "mushroom_melee": {
        "light": {
            "anim": "attack",
            "duration": 60 / 60,        # 1.0s
            "hitbox_start": 20 / 60,    # ~0.333s
            "hitbox_end": 30 / 60,      # 0.5s
            "hitbox": pygame.Rect(0, 0, 20, 20),
            "offsets": {
                "offset_x": 10,
                "offset_y": 10
            },
            "damage": 2
        }
    }
}