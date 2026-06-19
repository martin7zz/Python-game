import pygame
from physicsEntity import PhysicsEntity
from attackController import AttackController
from playerStates import *

from attacks import PLAYER_ATTACKS

class Player(PhysicsEntity, pygame.sprite.Sprite):
    def __init__(self, game, pos, size, is_Spawned, id, weapon):
        super().__init__(game, 'player', pos, size)
        pygame.sprite.Sprite.__init__(self)
        self.iid = id
        
        self.movement_state = MovementState.IDLE
        self.combat_state = CombatState.NEUTRAL
        
        self.speed_increment = 420
        self.air_time = 0
        self.doubleJump = True
        self.jumping = False
        self.current_jumps = 0
        self.max_jumps = 3
        self.jump_speed = 550
        self.dashing = 0
        self.grounded_timer = 0
        self.knockback_force = 300
        self.knockback_timer = 0
        self.damage_cooldown = 0
        
        self.combat = AttackController(self, PLAYER_ATTACKS)
        self.show_debug = True
        
        self.current_weapon = weapon
        self.attack_key_held = False
        self.weapon_level = 1
        
        self.movement = [False, False]
        self.prev_movement = [False, False]
        
        self.health = 4
        self.hit = False
        self.IsDead = False
        
        self.is_Spawned = is_Spawned
                
    def dash(self):
        if not self.dashing:
            if self.flip:
                self.dashing = -100
            else:
                self.dashing = 100
    
    def update_dash(self, dt):
        DASH_DECAY = 140
        DASH_THRESHOLD = 50
        FRICTION = 1400
        DASH_SPEED = 800

        # decay dash value
        if self.dashing > 0:
            self.dashing = max(0, self.dashing - DASH_DECAY * dt)
        elif self.dashing < 0:
            self.dashing = min(0, self.dashing + DASH_DECAY * dt)

        # active dash
        if abs(self.dashing) > DASH_THRESHOLD:
            self.velocity.x = DASH_SPEED if self.dashing > 0 else -DASH_SPEED

        # friction after dash
        else:
            if self.velocity.x > 0:
                self.velocity.x = max(0, self.velocity.x - FRICTION * dt)
            elif self.velocity.x < 0:
                self.velocity.x = min(0, self.velocity.x + FRICTION * dt)
    
    def jump(self):
        
        if self.grounded_timer > 0.04 and self.current_jumps == 0:
            self.doubleJump = False
            self.current_jumps = 1
        
        if self.current_jumps < self.max_jumps:
            self.current_jumps += 1
            self.velocity.y = -self.jump_speed
            self.air_time = 0
            self.jumping = True
    
    def update_air_state(self, dt):
        self.air_time += dt
        
        if self.collisions['down']:
            self.grounded_timer = 0
            self.air_time = 0
            self.current_jumps = 0
            self.doubleJump = True
        else:
            self.grounded_timer += dt
    
    def damage_cooldown_update(self, dt):
        self.damage_cooldown = max(0, self.damage_cooldown - dt)
            
    def update_knockback(self, dt):
        self.knockback_timer = max(0, self.knockback_timer - dt)
    
    def start_knockback(self, source):
        direction = 1 if self.rect().centerx >= source.rect().centerx else -1
        self.velocity.x = direction * self.knockback_force
        if self.is_airborne():
            self.velocity.y = direction + self.knockback_force - 600
        self.knockback_timer = 0.15
    
    def take_damage(self, amount, source=None):
        if self.IsDead:
            return
        if self.damage_cooldown > 0:
            return
        
        self.health -= amount
        self.hit = True
        
        self.damage_cooldown = 0.5
        
        if source is not None:
            self.start_knockback(source)
        
        if self.health <= 0:
            self.IsDead = True

    def check_enemy_hit(self, enemies):
        for enemy in enemies:
            if enemy.combat.hitbox_active:
                if not self.hit and self.rect().colliderect(enemy.combat.hitbox_rect):
                    self.take_damage(enemy.combat.get_damage(), enemy)
                    return
            elif self.rect().colliderect(enemy.rect()):
                self.take_damage(enemy.body_damage, enemy)
                return
            else:
                self.hit = False
            
    
    def handle_input(self):
        if self.knockback_timer > 0:
            return
        
        keys = pygame.key.get_pressed()
        
        left = keys[pygame.K_LEFT]
        right = keys[pygame.K_RIGHT]
        
        self.movement[0] = left
        self.movement[1] = right
        
        if left and not self.prev_movement[0]:
            self.last_dir = -1
        elif right and not self.prev_movement[1]:
            self.last_dir = 1

        if left and right:
            direction = self.last_dir
        elif left:
            direction = -1
        elif right:
            direction = 1
        else:
            direction = 0

        self.velocity.x = direction * self.speed_increment

        self.prev_movement = self.movement.copy()

        if keys[pygame.K_SPACE] or keys[pygame.K_UP]:
            if not self.jumping:
                self.jump()
        elif not keys[pygame.K_SPACE] and not keys[pygame.K_UP]:
            self.jumping = False
        
        if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
            self.dash()
        
        if keys[pygame.K_z]:
            if not self.attack_key_held:
                self.combat.attack_start(self.current_weapon, "light")
            self.attack_key_held = True
        else:
            self.attack_key_held = False
    
    def is_grounded(self):
        return self.collisions['down']
    
    def is_airborne(self):
        return self.grounded_timer > 0.04
    
    # def is_airborne(self):
    #     return not self.collisions['down']
    
    def update_states(self):
        # Comabt State
        if self.combat.active_attack:
            self.combat_state = CombatState.ATTACK
        elif self.knockback_timer > 0:
            self.combat_state = CombatState.KNOCKBACK
        else:
            self.combat_state = CombatState.NEUTRAL
        
        # Movement State
        if abs(self.dashing) > 50:
            self.movement_state = MovementState.DASH
        
        # elif self.is_airborne():
        #     if self.velocity.y < 0:
        #         self.movement_state = MovementState.JUMP
        #     else:
        #         self.movement_state = MovementState.FALL
        
        elif abs(self.velocity.x) > 0.1:
            self.movement_state = MovementState.RUN
        else:
            self.movement_state = MovementState.IDLE
    
    def update_animation(self):
        if self.combat_state == CombatState.ATTACK:
            if self.action != "attack":
                self.set_action("attack")
            return
        
        if self.movement_state == MovementState.IDLE:
            self.set_action("idle")
        elif self.movement_state == MovementState.RUN:
            self.set_action("run")
        # elif self.movement_state == MovementState.JUMP:
        #     self.set_action("jump")
        elif self.movement_state == MovementState.FALL:
            self.set_action("run")
        # elif self.movement_state == MovementState.DASH:
        #     self.set_action("dash")
    
    def update(self, tilemap, dt, movement=(0, 0)):
        eneimes = self.game.level.enemies
        
        self.update_knockback(dt)
        self.damage_cooldown_update(dt)
        self.update_states()
        
        self.handle_input()
        self.update_facing()
        self.update_dash(dt)
        
        super().update(tilemap, dt, movement=movement)
        
        self.combat.update(dt)
        self.check_enemy_hit(eneimes)
        
        self.update_air_state(dt)
        
        self.update_animation()
        
    def render(self, surf, camera):
        super().render(surf, camera)
        # FOR DEBUGGING
        self.combat.render(surf, camera)
    
    