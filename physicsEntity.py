import pygame
from spriteUtils import Animation
class PhysicsEntity():
    def __init__(self, game, e_type, pos, size, local_pos):
        self.game = game
        self.type = e_type
        self.pos = list(pos)
        self.local_pos = list(local_pos)
        self.size = size
        self.velocity = pygame.Vector2(0, 0)
        self.collisions = {'up': False, 'down': False, 'right': False, 'left': False}
        
        self.action = ''
        self.anim_offset = (-3, -3)
        self.flip = False
        
        self.animation = None
        self.set_action('idle')
        
        self.last_movement = (0, 0)
        
    def rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
    
    def set_action(self, action):
        if action != self.action:
            self.action = action
            key = self.type + '/' + self.action
            self.animation = self.game.assets.get(key).copy()
    
    def update(self, tilemap, movement=(0, 0)):
        self.collisions = {'up': False, 'down': False, 'right': False, 'left': False}
        
        frame_movement = (movement[0] + self.velocity.x, movement[1] + self.velocity.y)
        
        self.pos[0] += frame_movement[0]
        entity_rect = self.rect()
        for rect in tilemap.physics_rects_around(entity_rect):
            if entity_rect.colliderect(rect):
                if frame_movement[0] > 0:
                    entity_rect.right = rect.left
                    self.collisions['right'] = True
                if frame_movement[0] < 0:
                    entity_rect.left = rect.right
                    self.collisions['left'] = True
                self.pos[0] = entity_rect.x
        
        self.pos[1] += frame_movement[1]
        entity_rect = self.rect()
        for rect in tilemap.physics_rects_around(entity_rect):
             if entity_rect.colliderect(rect):
                if frame_movement[1] > 0:
                    entity_rect.bottom = rect.top
                    self.collisions['down'] = True
                    # print(f"collision down: {self.collisions['down']}")
                if frame_movement[1] < 0:
                    entity_rect.top = rect.bottom
                    self.collisions['up'] = True
                    # print(f"collision up: {self.collisions['up']}")
                self.pos[1] = entity_rect.y
        
        if movement[0] > 0:
            self.flip = False
        if movement[0] < 0:
            self.flip = True
        
        self.last_movement = movement
        
        # gravity
        if not self.collisions['down']:
            self.velocity.y = min(5, self.velocity.y + 0.18)
        
        if self.collisions['down'] or self.collisions['up']:
            self.velocity.y = 0
        
        # temporary
        if isinstance(self.animation, Animation):
            self.animation.update()
        
    def render(self, surf, camera):
        # frame = self.animation.img()

        # crop_rect = frame.get_bounding_rect()
        # cropped = frame.subsurface(crop_rect)

        # scaled = pygame.transform.scale(cropped, self.size)

        # flipped = pygame.transform.flip(scaled, self.flip, False)

        # draw_x = (self.pos[0] + camera[0])
        # draw_y = (self.pos[1] + camera[1])

        # surf.blit(flipped, (draw_x, draw_y))
        
        # debug_rect = pygame.Rect(draw_x, draw_y, *self.size)
        # pygame.draw.rect(surf, (255, 0, 0), debug_rect, 1)
        
        frame = self.animation.img()

        flipped = pygame.transform.flip(frame, self.flip, False)

        draw_x = (self.pos[0] + camera[0])
        draw_y = (self.pos[1] + camera[1])

        surf.blit(flipped, (draw_x, draw_y))
        
        debug_rect = pygame.Rect(draw_x, draw_y, *self.size)
        pygame.draw.rect(surf, (255, 0, 0), debug_rect, 1)
        