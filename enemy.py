import pygame
import math
import random
from physicsEntity import PhysicsEntity

class Enemy(PhysicsEntity, pygame.sprite.Sprite):
    def __init__(self, game, local_pos, world_pos, size, id):
        super().__init__(game, 'enemy', world_pos, size, local_pos)
        pygame.sprite.Sprite.__init__(self)
        
        self.walking = 0
        self.x, self.y = local_pos
        self.world_x, self.world_y = world_pos
        self.IsDead = False
        self.id = id
    
    def update(self, tilemap, movement=(0, 0)):
        if self.walking:
            foot_y = self.rect().bottom + 1
            front_x = self.rect().centerx + (-7 if self.flip else 7)

            if tilemap.solid_check((front_x, foot_y)):
                if (self.collisions["right"] or self.collisions["left"]):
                    self.flip = not self.flip
                else:
                    movement = (movement[0] - 1 if self.flip else 1, movement[1])
            else:
                self.flip = not self.flip
            self.walking = max(0, self.walking - 1)
            if not self.walking:
                # entity attack logic
                dis = (self.game.level.player.x - self.pos[0],
                       self.game.level.player.y - self.pos[1]
                )
                # if (abs(dis[1]) < 16):
                #     if (self.flip and dis[0] < 0):
                #         self.game.projectiles.append([[self.rect().centerx - 7, self.rect().centery], -1.5, 0])
                #         for i in range(4):
                #             self.game.sparks.append(Spark(self.game.projectiles[-1][0], random.random() - 0.5 + math.pi, 2 + random.random()))
                #     if (not self.flip and dis[0] > 0):
                #         self.game.projectiles.append([[self.rect().centerx + 7, self.rect().centery], 1.5, 0])
                #         for i in range(4):
                #             self.game.sparks.append(Spark(self.game.projectiles[-1][0], random.random() - 0.5, 2 + random.random()))
        elif random.random() < 0.01:
            self.walking = random.randint(30, 120)
        
        super().update(tilemap, movement=movement)
        
        if movement[0] != 0:
            self.set_action('run')
        else:
            self.set_action('idle')
        
        # player dash collision with entity
        if abs(self.game.level.player.dashing) >= 50:
            if self.rect().colliderect(self.game.level.player.rect()):
                return True
            else:
                return self.IsDead
    
    def render(self, surf, camera):
        super().render(surf, camera)
        
            