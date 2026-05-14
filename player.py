import pygame
from physicsEntity import PhysicsEntity

class Player(PhysicsEntity, pygame.sprite.Sprite):
    def __init__(self, game, pos, size, is_Spawned, id):
        super().__init__(game, 'player', pos, size)
        pygame.sprite.Sprite.__init__(self)
        self.iid = id
        
        self.speed_increment = 3.7
        self.air_time = 0
        self.doubleJump = True
        self.jumping = False
        self.current_jumps = 0
        self.max_jumps = 3
        self.jump_speed = 7.5
        self.dashing = 0
        self.grounded_timer = 0
        
        self.attack_hitbox = pygame.Rect(0, 0, 70, 30)
        self.attack_dir = 1
        self.show_debug = True
        
        self.attack_key_held = False
        self.attacking = False
        self.attack_timer = 0
        self.attack_duration = 50
        
        self.movement = [False, False]
        self.prev_movement = [False, False]
        
        self.health = 1000
        
        self.is_Spawned = is_Spawned
                
    def dash(self):
        if not self.dashing:
            if self.flip:
                self.dashing = -100
            else:
                self.dashing = 100
    
    def jump(self):
        
        if self.grounded_timer > 3 and self.current_jumps == 0:
            self.doubleJump = False
            self.current_jumps = 1
        
        if not self.doubleJump and self.current_jumps < self.max_jumps:
            self.current_jumps += 1
            self.velocity.y = -self.jump_speed
            self.air_time = self.jump_speed
            self.jumping = True
            # print(self.current_jumps)
        elif self.doubleJump and self.current_jumps < self.max_jumps:
            self.current_jumps += 1
            self.velocity.y = -self.jump_speed
            self.air_time = self.jump_speed
            self.jumping = True
            # print(self.current_jumps)
    
    def update_attack_hitbox(self):
        rect = self.rect()

        offset_x = 20

        center_x = rect.centerx

        if self.attack_dir == -1:
            self.attack_hitbox.x = center_x - offset_x - self.attack_hitbox.width
        else:
            self.attack_hitbox.x = center_x + offset_x

        self.attack_hitbox.y = rect.y + 10
       
    def attack(self):
        if not self.attacking:
            self.attacking = True
            self.attack_timer = self.attack_duration
            self.set_action('attack')
            
            self.attack_dir = -1 if self.flip else 1
            

            
    
    def handle_input(self):
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
                self.attack()
            self.attack_key_held = True
        else:
            self.attack_key_held = False
    
    def update(self, tilemap, movement=(0, 0)):
        self.handle_input()
        
        if self.dashing > 0:
            self.dashing = max(0, self.dashing - 1)
        if self.dashing < 0:
            self.dashing = min(0, self.dashing + 1)
        if abs(self.dashing) > 50:
            self.velocity.x = abs(self.dashing) / self.dashing * 8
            if abs(self.dashing) == 51:
                self.velocity.x *= 0.1
                
        if abs(self.dashing) <= 50:
            if self.velocity.x > 0:
                self.velocity.x = max(self.velocity.x - 0.1, 0)
            else:
                self.velocity.x = min(self.velocity.x + 0.1, 0)
        
        # print(self.velocity.x)
            
        super().update(tilemap, movement=movement)
        
        self.air_time += 1
        
        if not self.collisions['down']:
            self.grounded_timer += 1
        else:
            self.grounded_timer = 0  # Reset timer if grounded
        
        
        if self.collisions['down']:
            self.air_time = 0
            self.current_jumps = 0
            self.doubleJump = True
        
        if self.attacking:
            self.update_attack_hitbox()
        elif self.movement[0] or self.movement[1]:
            self.set_action('run')
        else:
            self.set_action('idle')
        
        if self.attacking:
            self.attack_timer -= 1

            if self.attack_timer <= 0:
                self.attacking = False
        
    
    def get_facing(self):
        if self.attacking:
            return self.attack_dir == -1
        return self.flip
    
    def render(self, surf, camera):
        super().render(surf, camera)
        
        if self.show_debug and self.attacking:
            debug_rect = pygame.Rect(
                self.attack_hitbox.x + camera[0],
                self.attack_hitbox.y + camera[1],
                self.attack_hitbox.width,
                self.attack_hitbox.height
            )

            pygame.draw.rect(surf, (255, 0, 0), debug_rect, 2)
    
    