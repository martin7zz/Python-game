import pygame

class AttackController:
    COMBO_BUFFER_WINDOW = 0.2
    def __init__(self, entity, attack_data):
        self.entity = entity
        self.attacks = attack_data
        
        self.active_attack = None
        self.timer = 0
        
        self.hitbox_active = False
        self.facing = 1
        
        self.hitbox_rect = pygame.Rect(0, 0, 0, 0)
    
    def get_damage(self):
        if not self.active_attack:
            return 0
        
        damage = self.active_attack.get("damage", 0)
        
        if isinstance(damage, dict):
            level = getattr(self.entity, "weapon_level", 1)
            return damage.get(level, damage[max(damage)])
        
        return damage    
    
    def attack_start(self, type, name):
        if self.active_attack:
            return
        
        self.active_attack = self.attacks[type][name]
        self.timer = self.active_attack["duration"]
        self.hitbox_active = False
        
        self.entity.set_action(self.active_attack["anim"])
        self.facing = -1 if self.entity.flip else 1
    
    def update(self, dt):
        if not self.active_attack:
            return

        self.timer -= dt
        
        elapsed = self.active_attack["duration"] - self.timer
        
        if self.active_attack["hitbox_start"] <= elapsed <= self.active_attack["hitbox_end"]:
            self.hitbox_active = True
        else:
            self.hitbox_active = False
        
        self.update_hitbox()
        
        if self.timer <= 0:
            self.active_attack = None
            self.hitbox_active = False
        
    def update_hitbox(self):
        if not self.active_attack:
            return

        base = self.active_attack["hitbox"]
        offsets = self.active_attack["offsets"]
        
        rect = self.entity.rect()
        
        self.hitbox_rect.width = base.width
        self.hitbox_rect.height = base.height
        
        if self.facing == 1:
            self.hitbox_rect.x = rect.centerx + offsets["offset_x"]
        else:
            self.hitbox_rect.x = rect.centerx - base.width - offsets["offset_x"]
        
        self.hitbox_rect.y = rect.y + offsets["offset_y"]

    # FOR DEBUGGING
    def render(self, surf, camera):

        if self.hitbox_active:

            debug_rect = pygame.Rect(
                self.hitbox_rect.x + camera[0],
                self.hitbox_rect.y + camera[1],
                self.hitbox_rect.width,
                self.hitbox_rect.height
            )

            pygame.draw.rect(surf, (255, 0, 0), debug_rect, 2)