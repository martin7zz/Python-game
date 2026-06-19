import pygame
import random
from enemy import Enemy
from enemyStates import *

class MushroomEnemy(Enemy):
    def __init__(self, game, pos, size, id):
        super().__init__(game, pos, size, id)
        self.patrol_speed = 60
        
        self.health = 100
        
        self.flip_x_override = True

    def get_ai_movement(self, tilemap, movement):
        if self.combat_state == CombatState.KNOCKBACK:
            movement = (self.velocity.x, movement[1])
            return movement
        
        if self.ai_state == AIState.PATROL:
            direction = -1 if self.flip else 1
            
            foot_y = self.rect().bottom + 1
            front_x = self.rect().centerx + (-7 if self.flip else 7)

            if tilemap.solid_check((front_x, foot_y)):
                if self.collisions["right"] or self.collisions["left"]:
                    self.flip = not self.flip
                else:
                    self.velocity.x = direction * self.patrol_speed
            else:
                self.flip = not self.flip
                self.velocity.x = 0
        else:
            self.velocity.x = 0

            self.walking = max(0, self.walking - 1)
        
        return movement
    
    def update_ai_actions(self):
        if self.ai_state == AIState.ATTACK:

            if not self.combat.active_attack:
                self.combat.attack_start("mushroom_melee", "light")
                self.attack_cooldown = 2
    
    def update_ai_state(self, dt):
        player = self.game.level.player
        
        dis = (
            player.rect().centerx - self.rect().centerx,
            player.rect().bottom - self.rect().bottom
        )

        facing_player = (
            (dis[0] > 0 and self.get_facing()) or
            (dis[0] < 0 and not self.get_facing())
        )
        if (
            facing_player and
            abs(dis[0]) < 45 and
            abs(dis[1]) < 30 and
            self.attack_cooldown <= 0
        ):
            self.ai_state = AIState.ATTACK
        # patrol state
        elif self.walking:
            self.ai_state = AIState.PATROL
        # idle state
        else:
            self.ai_state = AIState.IDLE
            
            PATROL_TRIGGER_RATE = 1.0 
            if random.random() < PATROL_TRIGGER_RATE  * dt:
                self.walking = random.uniform(0.5, 2.0)
    
    def ai_update(self, tilemap, dt, movement):
        self.update_ai_state(dt)

        self.update_ai_actions()
        
        movement = self.get_ai_movement(tilemap, movement)

        return movement