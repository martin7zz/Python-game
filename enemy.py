import pygame
import math
import random
from physicsEntity import PhysicsEntity
from attackController import AttackController
from enemyStates import *
from attacks import ENEMY_ATTACKS

class Enemy(PhysicsEntity, pygame.sprite.Sprite):
    def __init__(self, game, pos, size, id):
        super().__init__(game, 'enemy', pos, size)
        pygame.sprite.Sprite.__init__(self)
        self.ai_state = AIState.IDLE
        self.movement_state = MovementState.IDLE
        self.combat_state = CombatState.NEUTRAL
        
        self.health = 100
        self.walking = 0
        self.IsDead = False
        self.id = id
        
        self.combat = AttackController(self, ENEMY_ATTACKS)
        self.hit = False
        self.body_damage = 1
        
        self.knockback_force = 500
        self.knockback_timer = 0
        
        self.attack_cooldown = 0
    
    def update_attack_cooldown(self, dt):
        self.attack_cooldown = max(0, self.attack_cooldown - dt)
    
    def update_knockback(self, dt):
        self.knockback_timer = max(0, self.knockback_timer - dt)
    
    def start_knockback(self, source):
        direction = 1 if self.rect().centerx >= source.rect().centerx else -1
        self.velocity.x = direction * self.knockback_force
        self.knockback_timer = 0.15
    
    def take_damage(self, amount, source=None):
        if self.IsDead:
            return
        self.health -= amount
        self.hit = True
        
        if source is not None:
            self.start_knockback(source)
        
        if self.health <= 0:
            self.IsDead = True
    
    def check_player_hit(self, player):
        if player.combat.hitbox_active:
            if not self.hit and self.rect().colliderect(player.combat.hitbox_rect):
                self.take_damage(player.combat.get_damage(), player)
        else:
            self.hit = False
    
    def is_grounded(self):
        return self.collisions['down']
    
    def is_airborne(self):
        return not self.collisions['down']
    
    def update_states(self):
        # Comabt State
        if self.knockback_timer > 0:
            self.combat_state = CombatState.KNOCKBACK
        elif self.combat.active_attack:
            self.combat_state = CombatState.ATTACK
        else:
            self.combat_state = CombatState.NEUTRAL
        
        
        if self.is_airborne():
            if self.velocity.y < 0:
                self.movement_state = MovementState.JUMP
            else:
                self.movement_state = MovementState.FALL
        
        elif abs(self.velocity.x) > 0.1:
            self.movement_state = MovementState.RUN
        else:
            self.movement_state = MovementState.IDLE
            
    
    def update_animation(self):
        if self.combat_state == CombatState.ATTACK:
            self.set_action("attack")
            return
        
        if self.movement_state == MovementState.IDLE:
            self.set_action("idle")
        elif self.movement_state == MovementState.RUN:
            self.set_action("run")
    
    def update(self, tilemap, dt, movement=(0, 0)):
        player = self.game.level.player

        self.update_knockback(dt)
        
        self.update_states()
        
        movement = self.ai_update(tilemap, dt, movement)
        
        self.update_facing()

        super().update(tilemap, dt, movement=movement)
        
        
        self.combat.update(dt)
        
        self.check_player_hit(player)
        
        self.update_animation()

        self.update_attack_cooldown(dt)
        
        return self.IsDead
    
    def ai_update(self, tilemap, dt, movement):
        return movement
    
    def render(self, surf, camera):
        super().render(surf, camera)
        self.combat.render(surf, camera)
        
            